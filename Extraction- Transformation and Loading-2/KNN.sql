create procedure usp_knn
	@temperature varchar(10)
as
begin
decalre @sql varchar(max)
set @sql='SELECT
    *
FROM (
    SELECT
        *
      , ROW_NUMBER() OVER (ORDER BY ABS( Launch_temperature-'+@temperature+')) AS rn
    FROM challenger
) AS d
WHERE rn = 1'
exec @sql;
end



--the other way of doing things
select top 1 * from challenger 
order by 
abs(Launch_temperature-70) ASC