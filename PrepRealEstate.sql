SELECT
  property_purchase_price,
  equity_ratio,
  interest_rate,
  loan_term,
  amortization_period,
  annual_growth_rate,
  annual_rent_growth_rate,
  exit_cap_rate,
  investment_horizon,
  equity_irr_threshold,
  annual_rent_income,
  annual_expenses,
  tax_rate
FROM
  real_estate_properties
WHERE
  property_type = 'residential'
