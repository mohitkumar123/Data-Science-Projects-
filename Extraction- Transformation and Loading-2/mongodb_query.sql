CREATE PROCEDURE 
usp_mongodb @id int,
@jsoninfo VARCHAR(MAX) output
AS
begin
-- declare variable
--DECLARE @json VARCHAR(MAX)
--DECLARE @jsonInfo VARCHAR(MAX)
DECLARE @user_id INT
DECLARE @order_id INT
DECLARE @order_number INT
DECLARE @order_dow INT
DECLARE @days_since_prior_order VARCHAR(MAX)
DECLARE @add_to_cart_order INT
DECLARE @reordered INT
DECLARE @product_name VARCHAR(MAX)
DECLARE @department VARCHAR(MAX)
DECLARE @aisle VARCHAR(MAX)

-- declare cursor
DECLARE cursor_results CURSOR FOR
SELECT * FROM orders_denorm WHERE order_id=@id 
-- process the cursor row by row
OPEN cursor_results
	FETCH NEXT FROM cursor_results into @user_id, @order_id, @order_number, 
		@order_dow, @days_since_prior_order, @add_to_cart_order, @reordered, 
		@product_name, @department, @aisle
	set @jsonInfo = JSON_MODIFY('{}', '$.user_id', @user_id)
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.order_id', @order_id)
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.order_number', @order_number)
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.order_dow', @order_dow)
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.days_since_prior_order', @days_since_prior_order)
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.add_to_cart_order', JSON_QUERY('[]'))
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.reordered', JSON_QUERY('[]'))
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.product_names', JSON_QUERY('[]'))
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.departments', JSON_QUERY('[]'))
	set @jsonInfo = JSON_MODIFY(@jsonInfo, '$.aisles', JSON_QUERY('[]'))
	WHILE @@FETCH_STATUS = 0
		BEGIN 			
			set @jsonInfo = JSON_MODIFY(@jsonInfo, 'append $.add_to_cart_order', @add_to_cart_order)			
			set @jsonInfo = JSON_MODIFY(@jsonInfo, 'append $.reordered', @reordered)			
			set @jsonInfo = JSON_MODIFY(@jsonInfo, 'append $.product_names', @product_name)			
			set @jsonInfo = JSON_MODIFY(@jsonInfo, 'append $.departments', @department)			
			set @jsonInfo = JSON_MODIFY(@jsonInfo, 'append $.aisles', @aisle)
			FETCH NEXT FROM cursor_results into @user_id, @order_id, @order_number, 
		@order_dow, @days_since_prior_order, @add_to_cart_order, @reordered, 
		@product_name, @department, @aisle
		end;
	close cursor_results
	deallocate cursor_results 
end;

