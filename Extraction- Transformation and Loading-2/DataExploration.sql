-- 1. KNN classification model
drop procedure if exists usp_knn
create procedure usp_knn (@temperature varchar(10))
as
declare @seq varchar(max)
set @seq='select * from challenger 
where sqrt(square(Launch_temperature-'+@temperature+'))=
(select min(sqrt(square(Launch_temperature-'+@temperature+'))) from challenger)'
exec (@seq)

exec usp_knn @temperature='70'

--second method:
select top 1 * from challenger 
order by 
abs(Launch_temperature-70) ASC

--third way of doing things:
drop procedure if exists usp_knn
create procedure usp_knn
	@temperature varchar(10)
as
begin
declare @sql varchar(max)
set @sql='SELECT
    *
FROM (
    SELECT
        *
      , ROW_NUMBER() OVER (ORDER BY ABS( Launch_temperature-'+@temperature+')) AS rn
    FROM challenger
) AS d
WHERE rn = 1'
exec (@sql);
end

-- 2. Recommendation system
drop table if exists RS
create table RS (ProductA int, ProductB int, Frq int)

-- declare variable
DECLARE @oid INT
DECLARE @prod1 INT
DECLARE @prod2 INT
DECLARE @freq INT
-- declare cursor
DECLARE cursor_results CURSOR FOR
SELECT distinct(order_id) FROM order_products_train order by order_id
-- process the cursor row by row
OPEN cursor_results
	FETCH NEXT FROM cursor_results into @oid
	WHILE @@FETCH_STATUS = 0
		BEGIN 
		DECLARE cursor_results2 CURSOR FOR
		select a.product_id, b.product_id 
			from order_products_train a, order_products_train b 
			where a.order_id=@oid and b.order_id=@oid and a.product_id<b.product_id
			OPEN cursor_results2
				FETCH NEXT FROM cursor_results2 into @prod1, @prod2
				WHILE @@FETCH_STATUS = 0
					BEGIN
						if exists (select *
							from RS where ProductA=@prod1 and ProductB=@prod2)
							begin
							set @freq= (select Frq from RS 
								where ProductA=@prod1 and ProductB=@prod2)+1
							update RS set Frq=@freq 
							where ProductA=@prod1 and ProductB=@prod2
							end
						if not exists (select *
							from RS where ProductA=@prod1 and ProductB=@prod2)
							begin
							insert into RS values (@prod1,@prod2,1)
							end
						FETCH NEXT FROM cursor_results2 into @prod1, @prod2
					END
			CLOSE cursor_results2
			DEALLOCATE cursor_results2
			FETCH NEXT FROM cursor_results into @oid
		END
CLOSE cursor_results
-- clean up
DEALLOCATE cursor_results

-- stored procedure recommendation
drop procedure if exists usp_rs
create procedure usp_rs (@product varchar(10))
as
declare @seq varchar(max)
set @seq='select top 3 * from RS
			where ProductA='+@product+'or ProductB='+@product+'order by Frq DESC'
exec (@seq)

usp_rs '13176'

