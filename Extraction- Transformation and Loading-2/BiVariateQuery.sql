create procedure usp_bivariate
	@tbl varchar(200),
	@target_colname varchar(100),
	@predictor_colname varchar(100)
as
begin
	declare @sql varchar(max)
	set @sql='with cte1(mean1,mean2, var1, var2, count1, count2) as ( select avg('+@target_colname+') as mean1, var('+@target_colname
	+') as var1,count('+@target_colname+') as count1, avg('+@predictor_colname+') as mean2, var('+@predictor_colname
	+') as var2,count('+@predictor_colname+') as count2 from '+@tbl+') select (mean1-mean2)/sqrt(var1/count1+var2/count2) from cte1' 
	exec(@sql)
end