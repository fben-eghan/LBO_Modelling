import numpy as np
import numpy_financial as npf
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns


class RealEstateInvestment:
    
    def __init__(self, p=1e6, e=0.25, r=0.06, lt=10, ap=25, agr=0.02, arg=0.02,
                 ecr=0.08, ih=5, irr=0.15, ri=5e4, ex=2.5e4, t=0.2):
        """
        Initialize the RealEstateInvestment class with default values.
        
        Parameters:
           p (float): Purchase price of the property
           e (float): Equity investment as a percentage of the purchase price
           r (float): Annual interest rate on the mortgage
           lt (int): Length of the mortgage in years
           ap (int): Amortization period of the mortgage in years
           agr (float): Annual growth rate of rental income
           arg (float): Annual growth rate of the resale value of the property
           ecr (float): Expected capitalization rate of the property
           ih (int): Holding period of the property in years
           irr (float): Target internal rate of return
           ri (float): Annual rental income from the property
           ex (float): Annual property expenses
           t (float): Marginal tax rate
        """
        self.p, self.e, self.r, self.lt, self.ap, self.agr = p, e, r, lt, ap, agr
        self.arg, self.ecr, self.ih, self.irr, self.ri, self.ex, self.t = arg, ecr, ih, irr, ri, ex, t
        self.d, self.pmt, self.noi = None, None, None
        self.iters = 10000
        self.p_dist, self.ri_dist, self.ex_dist = None, None, None
        self.agr_dist, self.arg_dist, self.ecr_dist = None, None, None
        self.irr_dist = np.zeros(self.iters)

    def calculate(self, num_sims=10000, **kwargs):
        """
        Simulate cash flows and calculate the probability of achieving the desired IRR.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        res = []
        for _ in range(num_sims):
            # Calculate down payment and equity.
            self.d, self.e = self.e * self.p, (1 - self.e) * self.p
            
            # Calculate monthly payment, net operating income, and annual cash flows.
            self.pmt = npf.pmt(self.r / 12, self.lt * 12, -self.d, 0)
            self.noi = self.ri - self.ex
            annual_cash_flow_before_tax = self.noi - (self.r * self.d + self.pmt) * 12
            annual_cash_flow_after_tax = annual_cash_flow_before_tax * (1 - self.t)
            
            # Calculate terminal value and cash flows.
            terminal_value = annual_cash_flow_before_tax * (1 + self.arg) / (self.ecr - self.arg)
            cash_flows = [-self.e] + [annual_cash_flow_after_tax] * self.ih + [terminal_value]
            
            # Calculate IRR and append result to res list.
            self.irr_dist[_] = npf.irr(cash_flows)
            res.append(1 if self.irr_dist[_] >= self.irr else 0)
        
        # Calculate probability of achieving the desired IRR.
        return sum(res) / num_sims

#Create many instances of the RealEstateInvestment class

num_sims = 10000
results = [RealEstateInvestment().calculate(num_sims) for _ in range(num_sims)]

sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(8, 6))

sns.histplot(results, ax=ax, bins=40, kde=True, stat='density',
color='tab:blue', alpha=0.8, line_kws={'linewidth': 2})
sns.kdeplot(results, ax=ax, color='tab:orange', linewidth=3)

ax.set_xlabel('IRR Probability', fontsize=14)
ax.set_ylabel('Density', fontsize=14)
ax.set_title('Distribution of IRR Probability', fontsize=16)
ax.legend(['Kernel Density Estimate', 'Histogram'], fontsize=12)

plt.show()
