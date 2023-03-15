import numpy as np
import numpy_financial as npf


class LBOTransaction:
    def __init__(self, purchase_price, financing_amount, financing_interest_rate, holding_period, rental_income,
                 expenses, capex, exit_cap_rate):
        self.purchase_price = purchase_price
        self.financing_amount = financing_amount
        self.financing_interest_rate = financing_interest_rate
        self.holding_period = holding_period
        self.rental_income = rental_income
        self.expenses = expenses
        self.capex = capex
        self.exit_cap_rate = exit_cap_rate

    def calculate_cash_flows(self):
        # Calculate projected cash flows for the holding period
        rental_income_cf = np.repeat(self.rental_income, self.holding_period)
        expenses_cf = np.repeat(self.expenses, self.holding_period)
        capex_cf = np.repeat(self.capex, self.holding_period)
        net_income_cf = rental_income_cf - expenses_cf
        ebitda_cf = net_income_cf + capex_cf
        debt_service_cf = -npf.pmt(self.financing_interest_rate / 12, self.holding_period * 12, self.financing_amount)
        unlev_cf = ebitda_cf + debt_service_cf
        terminal_value = unlev_cf[-1] / self.exit_cap_rate
        terminal_cf = np.repeat(terminal_value, self.holding_period)
        cash_flows = np.concatenate((unlev_cf, terminal_cf))
        return cash_flows

    def calculate_irr_probability(self, targ_irr, iterations=10000):
        # Calculate probability of meeting a given IRR using Monte Carlo simulation
        cash_flows = self.calculate_cash_flows()
        npv_values = []
        for i in range(iterations):
            discount_rate = np.random.normal(self.financing_interest_rate, 0.01)
            npv_value = npf.npv(discount_rate, cash_flows)
            npv_values.append(npv_value)
        irr_values = npf.irr(np.array([-self.purchase_price] + npv_values))
        prob = sum(irr_values >= targ_irr) / iterations
        return prob


# Example usage
transaction = LBOTransaction(purchase_price=1000000, financing_amount=800000, financing_interest_rate=0.05,
                             holding_period=10, rental_income=120000, expenses=60000, capex=20000, exit_cap_rate=0.06)
target_irr = 0.15
probability = transaction.calculate_irr_probability(target_irr)
print(f"Probability of meeting target IRR of {target_irr}: {probability:.2f}")
