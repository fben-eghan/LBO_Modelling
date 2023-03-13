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

    def calculate(self):
        for i in range(self.iterations):
            # Generate random values for input parameters
            purchase_price = self.purchase_price_dist.rvs()
            annual_rent_income = self.annual
