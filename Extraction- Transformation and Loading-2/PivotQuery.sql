
select department, aisle, "0" as Monday, "1" as Tuesday, "2" as Wednesday, 
	"3" as Thursday, "4" as Friday, "5" as Saturday, "6" as Sunday into MyPivot
	from
	(select a.aisle, d.department, order_dow, sale_price
	from facttable f
	inner join aisles a 
		on f.aisle_id=a.aisle_id
	inner join departments d
		on f.department_id=d.department_id) p
	
	PIVOT(sum(sale_price) FOR order_dow IN("0","1","2","3","4","5","6")) AS pvt

