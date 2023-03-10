import numpy as np
import pandas as pd

class RealEstateInvestment:
    
    def __init__(self, purchase_price, equity_ratio, interest_rate, loan_term, amortization_period,
                 annual_growth_rate, annual_rent_growth_rate, exit_cap_rate, investment_horizon,
                 equity_IRR_threshold, annual_rent_income, annual_expenses, tax_rate):
        
        self.purchase_price = purchase_price
        self.equity_ratio = equity_ratio
        self.interest_rate = interest_rate
        self.loan_term = loan_term
        self.amortization_period = amortization_period
        self.annual_growth_rate = annual_growth_rate
        self.annual_rent_growth_rate = annual_rent_growth_rate
        self.exit_cap_rate = exit_cap_rate
        self.investment_horizon = investment_horizon
        self.equity_IRR_threshold = equity_IRR_threshold
        self.annual_rent_income = annual_rent_income
        self.annual_expenses = annual_expenses
        self.tax_rate = tax_rate
        
    def calculate_debt_and_equity_amounts(self):
        self.debt_amount = (1 - self.equity_ratio) * self.purchase_price
        self.equity_amount = self.purchase_price - self.debt_amount
    
    def calculate_debt_service_payments(self):
        interest_payment = self.interest_rate * self.debt_amount
        principal_payment = np.pmt(self.interest_rate / 12, self.loan_term * 12, -self.debt_amount, 0)
        self.debt_service_payment = interest_payment + principal_payment
        
    def calculate_annual_cash_flows(self):
        annual_debt_service = self.debt_service_payment * 12
        annual_net_operating_income = self.annual_rent_income - self.annual_expenses
        annual_cash_flow_before_tax = annual_net_operating_income - annual_debt_service
        self.annual_cash_flow_after_tax = annual_cash_flow_before_tax * (1 - self.tax_rate)
    
    def calculate_terminal_value(self):
        self.terminal_value = self.annual_cash_flow_after_tax * (1 + self.annual_rent_growth_rate) / (self.exit_cap_rate - self.annual_rent_growth_rate)
    
    def calculate_equity_IRR(self):
        cash_flows = [-(self.equity_amount)] + [self.annual_cash_flow_after_tax] * self.investment_horizon + [self.terminal_value]
        self.equity_IRR = np.irr(cash_flows)
    
    def is_meeting_equity_IRR_threshold(self):
        return self.equity_IRR >= self.equity_IRR_threshold
    
    def run_analysis(self, scenario_params):
        scenario_results = []
        for param_value in scenario_params:
            setattr(self, param_value[0], param_value[1])
            self.calculate_debt_and_equity_amounts()
            self.calculate_debt_service_payments()
            self.calculate_annual_cash_flows()
            self.calculate_terminal_value()
            self.calculate_equity_IRR()
            scenario_results.append((param_value[0], param_value[1], self.equity_IRR
