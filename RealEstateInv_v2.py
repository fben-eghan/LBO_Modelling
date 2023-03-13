import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


class RealEstateInvestment:
    def __init__(self, purchase_price=1000000, equity_ratio=0.25, interest_rate=0.06, loan_term=10,
                 amortization_period=25, annual_growth_rate=0.02, annual_rent_growth_rate=0.02,
                 exit_cap_rate=0.08, investment_horizon=5, equity_IRR_threshold=0.15,
                 annual_rent_income=50000, annual_expenses=25000, tax_rate=0.2):

        self.purchase_price = purchase_price  # property purchase price
        self.equity_ratio = equity_ratio  # proportion of purchase price paid with equity
        self.debt_ratio = 1 - equity_ratio  # proportion of purchase price financed with debt
        self.interest_rate = interest_rate  # annual interest rate on the loan
        self.loan_term = loan_term  # term of the loan in years
        self.amortization_period = amortization_period  # period over which the loan is amortized
        self.annual_growth_rate = annual_growth_rate  # annual growth rate of the property value
        self.annual_rent_growth_rate = annual_rent_growth_rate  # annual growth rate of the rental income
        self.exit_cap_rate = exit_cap_rate  # capitalization rate at which the property is sold
        self.investment_horizon = investment_horizon  # investment horizon in years
        self.equity_IRR_threshold = equity_IRR_threshold  # minimum required equity IRR
        self.annual_rent_income = annual_rent_income  # annual rental income
        self.annual_expenses = annual_expenses  # annual property expenses
        self.tax_rate = tax_rate  # marginal tax rate of the investor
        
        # Initialize variables for Monte Carlo simulation
        self.iterations = 10000  # number of Monte Carlo iterations
        self.purchase_price_dist = norm(loc=purchase_price, scale=purchase_price*0.05)  # normal distribution for purchase price
        self.annual_rent_income_dist = norm(loc=annual_rent_income, scale=annual_rent_income*0.05)  # normal distribution for annual rent income
        self.annual_expenses_dist = norm(loc=annual_expenses, scale=annual_expenses*0.05)  # normal distribution for annual expenses
        self.annual_growth_rate_dist = norm(loc=annual_growth_rate, scale=annual_growth_rate*0.05)  # normal distribution for annual growth rate
        self.annual_rent_growth_rate_dist = norm(loc=annual_rent_growth_rate, scale=annual_rent_growth_rate*0.05)  # normal distribution for annual rent growth rate
        self.exit_cap_rate_dist = norm(loc=exit_cap_rate, scale=exit_cap_rate*0.05)  # normal distribution for exit cap rate
        self.equity_IRR_dist = np.zeros(self.iterations)  # initialize array to store equity IRR results

    
    def calculate(self, num_simulations):
        results = []
        for i in range(num_simulations):
            # Calculate the debt and equity amounts
            debt_amount = self.debt_ratio * self.purchase_price
            equity_amount = self.purchase_price - debt_amount

            # Calculate the debt service payments
            interest_payment = self.interest_rate * debt_amount
            principal_payment = np.pmt(self.interest_rate / 12, self.loan_term * 12, -debt_amount, 0)
            debt_service_payment = interest_payment + principal_payment

            # Calculate the annual cash flows
            annual_debt_service = debt_service_payment * 12
            annual_net_operating_income = self.annual_rent_income - self.annual_expenses
            annual_cash_flow_before_tax = annual_net_operating_income - annual_debt_service
            annual_cash_flow_after_tax = annual_cash_flow_before_tax * (1 - self.tax_rate)
            
            # Calculate the terminal value
            terminal_value = annual_cash_flow_before_tax * (1 + self.annual_rent_growth_rate) / (self.exit_cap_rate - self.annual_rent_growth_rate)

            # Calculate the equity IRR
            cash_flows = [-(equity_amount)] + [annual_cash_flow_after_tax] * self.investment_horizon + [terminal_value]
            equity_irr = np.irr(cash_flows)

            # Determine whether the investment meets the minimum equity IRR threshold
            if equity_irr >= self.equity_IRR_threshold:
                results.append(1)
            else:
                results.append(0)

        success_rate = sum(results) / num_simulations
        return success_rate

# Create an instance of the RealEstateInvestment class
rei = RealEstateInvestment()

# Call the calculate method with 10000 simulations and print the success rate
num_simulations = 10000
success_rate = rei.calculate(num_simulations)
print(f"Success rate after {num_simulations} simulations: {success_rate:.2%}")

