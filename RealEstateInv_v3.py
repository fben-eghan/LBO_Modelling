import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

class RealEstateInvestment:
    def __init__(self, p=1e6, e=0.25, r=0.06, lt=10, ap=25, agr=0.02, arg=0.02,
                 ecr=0.08, ih=5, irr=0.15, ri=5e4, ex=2.5e4, t=0.2):
        self.p, self.e, self.r, self.lt, self.ap, self.agr = p, e, r, lt, ap, agr
        self.arg, self.ecr, self.ih, self.irr, self.ri, self.ex, self.t = arg, ecr, ih, irr, ri, ex, t
        self.d, self.pmt, self.noi = None, None, None
        self.iters = 10000
        self.p_dist, self.ri_dist, self.ex_dist = None, None, None
        self.agr_dist, self.arg_dist, self.ecr_dist = None, None, None
        self.irr_dist = np.zeros(self.iters)

    def calculate(self, num_sims):
        res = []
        for _ in range(num_sims):
            self.d, self.e = self.e * self.p, (1 - self.e) * self.p
            self.pmt = np.pmt(self.r / 12, self.lt * 12, -self.d, 0)
            self.noi = self.ri - self.ex
            annual_cash_flow_before_tax = self.noi - (self.r * self.d + self.pmt) * 12
            annual_cash_flow_after_tax = annual_cash_flow_before_tax * (1 - self.t)
            terminal_value = annual_cash_flow_before_tax * (1 + self.arg) / (self.ecr - self.arg)
            cash_flows = [-self.e] + [annual_cash_flow_after_tax] * self.ih + [terminal_value]
            self.irr_dist[_] = np.irr(cash_flows)
            res.append(1 if self.irr_dist[_] >= self.irr else 0)
        return sum(res) / num_sims

# assuming you have already instantiated the RealEstateInvestment class and defined the calculate method

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
