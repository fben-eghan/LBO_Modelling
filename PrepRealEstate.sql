SELECT
    p.property_purchase_price,  /* select the property purchase price from the property table */
    l.equity_ratio,  /* select the equity ratio from the loan table */
    l.interest_rate,  /* select the interest rate from the loan table */
    l.loan_term,  /* select the loan term from the loan table */
    l.amortization_period,  /* select the amortization period from the loan table */
    r.annual_growth_rate,  /* select the annual growth rate from the rental table */
    r.annual_rent_growth_rate,  /* select the annual rent growth rate from the rental table */
    r.annual_rent_income,  /* select the annual rent income from the rental table */
    r.annual_expenses  /* select the annual expenses from the rental table */
FROM
    property p
JOIN
    loan l ON p.property_id = l.property_id  /* join the property and loan tables on property_id */
JOIN
    rental r ON p.property_id = r.property_id  /* join the property and rental tables on property_id */
GROUP BY
    p.property_purchase_price,  /* group the results by property purchase price */
    l.equity_ratio,  /* group the results by equity ratio */
    l.interest_rate,  /* group the results by interest rate */
    l.loan_term,  /* group the results by loan term */
    l.amortization_period,  /* group the results by amortization period */
    r.annual_growth_rate,  /* group the results by annual growth rate */
    r.annual_rent_growth_rate,  /* group the results by annual rent growth rate */
    r.annual_rent_income,  /* group the results by annual rent income */
    r.annual_expenses  /* group the results by annual expenses */

ORDER BY 
  p.property_purchase_price ASC;


-- The above query can be used to prepare scenario data for RealEstateInv.py
