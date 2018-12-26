
create procedure usp_mongodb_ex
as
begin
create table jsontable(JSONINFORMATION varchar(max));

declare @json VARCHAR(MAX)
set @json=''
declare @My_id int
DECLARE id_cursor CURSOR FOR
SELECT distinct order_id FROM orders_denorm 
-- process the cursor row by row
OPEN id_cursor
	fetch next from id_cursor into @My_id
	while @@FETCH_STATUS=0
	begin
	set @json=''
	exec usp_mongodb @My_id, @jsoninfo=@json output;
	insert into jsontable
		values(@json);
	fetch next from id_cursor into @My_id
	end;
CLOSE id_cursor;
deallocate id_cursor;
end;