create procedure usp_univariate
	@tbl varchar(200),
	@col varchar(100)
as
begin
	declare @sql varchar(max)
	--count
	set @sql='select count(' + @col + ') from' + @tbl
	exec(@sql)
	--average 	
	set @sql='select avg('+@col+') from '+@tbl
	exec(@sql)
	--median
	--To be continued

	--mode
	--to be continued

	--rane?

	--Variance 
	set @sql='select var(' + @col + ') from '+ @tbl
	exec(@sql)
	--Standrad Deviation 
	set @sql='select stdev(' + @col + ') from' + @tbl
	exec(@sql)
	--Coefficient of Variation
	set @sql='select stdev(' + @col +')/avg(' +@col + ') from ' + @tbl
	exec(@sql);
end

