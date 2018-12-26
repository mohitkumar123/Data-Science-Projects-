select *  into dbo.facttable from dbo.orders_denorm
go

select top 1000 * from dbo.facttable
go


alter table dbo.facttable add aisle_id int, department_id int, product_id int; 
go


declare @Product nvarchar(50)
declare @Ais nvarchar(50)
declare @Department nvarchar(50)
declare @Product_id int
declare @Ais_id int 
declare @Department_id int

declare StarSchema cursor dynamic 
for select  aisle, department, product_name from dbo.facttable
for update of aisle_id, department_id, product_id;

open StarSchema 
fetch next from StarSchema into @Ais, @Department, @Product;
while @@FETCH_STATUS=0
begin
	select @Ais_id=dbo.aisles.aisle_id from dbo.aisles where dbo.aisles.aisle=@Ais
	select @Department_id=dbo.departments.department_id from dbo.departments where dbo.departments.department=@Department
	select @Product_id=dbo.products.product_id from dbo.products where dbo.products.aisle_id=@Ais_id and dbo.products.department_id=@Department_id
	update dbo.facttable set aisle_id=@Ais_id, department_id=@Department_id, product_id=@Product_id where current of StarSchema 
	fetch next from StarSchema into @Ais, @Department, @Product;
end
close StarSchema
deallocate StarSchema
