-- This query selects data from the Property table and joins it with the Rent table and Expense table
-- to calculate annual_rent_income and annual_expenses fields respectively
SELECT 
    p.PropertyID, 
    p.PurchasePrice, 
    p.YearBuilt, 
    p.SquareFootage, 
    r.AnnualRent AS annual_rent_income, 
    SUM(e.Amount) AS annual_expenses
FROM 
    Property p
    LEFT JOIN Rent r ON p.PropertyID = r.PropertyID
    LEFT JOIN Expense e ON p.PropertyID = e.PropertyID
GROUP BY 
    p.PropertyID, 
    p.PurchasePrice, 
    p.YearBuilt, 
    p.SquareFootage, 
    r.AnnualRent

-- The above query can be used to populate the annual_rent_income and annual_expenses fields in RealEstateInvestment.py
