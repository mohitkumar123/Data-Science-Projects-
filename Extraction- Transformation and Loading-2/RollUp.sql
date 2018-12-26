SELECT department, aisle, SUM(Monday)as MonSales, SUM(Tuesday)as TueSales, 
SUM(Wednesday)as WedSales, SUM(Thursday)as ThsSales, SUM(Friday)as FriSales, 
SUM(Saturday)as SatSales, SUM(Sunday)as SunSales, GROUPING(department) 
AS 'Grouping' 
FROM MyPivot
GROUP BY department, aisle with rollup
ORDER BY 1,2