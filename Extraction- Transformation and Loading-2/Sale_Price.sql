use Instacart
go

alter table dbo.orders_denorm add sale_price real;
go

declare @RANDOM real;
declare @TEMP real;
declare Cursor_Update cursor

for select sale_price from dbo.orders_denorm 
for update of sale_price;

open Cursor_Update
fetch next from Cursor_Update into @TEMP
while(@@FETCH_STATUS=0)
begin
	set @RANDOM=1+99*RAND()
	update dbo.orders_denorm set sale_price=@RANDOM where current of Cursor_Update
	fetch next from Cursor_Update into @TEMP
end

close Cursor_Update
deallocate Cursor_Update;