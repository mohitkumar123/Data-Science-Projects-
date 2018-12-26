use Instacart
go
--slicing
select aisle, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday 
	from dbo.MyPivot
	where department='produce'

--dicing
select Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday 
	from dbo.MyPivot
	where  department like 'f%'  and aisle like 'f%'