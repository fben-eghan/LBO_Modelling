import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from RealEstateInvestment import RealEstateInvestment

# Load cash flows from SQL database
cash_flows = pd.read_sql_query("SELECT * FROM cash_flows", conn)

# Preprocess data
X = cash_flows.drop(columns=['IRR'])
y = cash_flows['IRR']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict IRR for a new set of cash flows
new_cash_flows = pd.read_sql_query("SELECT * FROM new_cash_flows", conn)
X_new = new_cash_flows.drop(columns=['IRR'])
y_pred = rf.predict(X_new)

# Instantiate a RealEstateInvestment object and calculate the probability of meeting the target IRR
p = new_cash_flows['Purchase_Price'][0]
e = new_cash_flows['Equity_Investment'][0]
r = new_cash_flows['Annual_Interest_Rate'][0]
lt = new_cash_flows['Mortgage_Length'][0]
ap = new_cash_flows['Amortization_Period'][0]
agr = new_cash_flows['Annual_Growth_Rate_Rental_Income'][0]
arg = new_cash_flows['Annual_Growth_Rate_Resale_Value'][0]
ecr = new_cash_flows['Expected_Capitalization_Rate'][0]
ih = new_cash_flows['Holding_Period'][0]
ri = new_cash_flows['Annual_Rental_Income'][0]
ex = new_cash_flows['Annual_Expenses'][0]
t = new_cash_flows['Marginal_Tax_Rate'][0]
irr = y_pred[0]
real_estate_investment = RealEstateInvestment(p, e, r, lt, ap, agr, arg, ecr, ih, irr, ri, ex, t)
probability = real_estate_investment.calculate()
