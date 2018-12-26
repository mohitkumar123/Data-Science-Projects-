--Final Example Preparation 

--BEGIN/COMMIT/ROLLBACK TRANSACTION
create table valuetable(id int);
go

begin transaction;
	insert into valuetable values(1);
	insert into valuetable values(2);
rollback transaction; 

--if else
if (select count(*) from valuetable)=0
	print 'no';
else
	print 'yes';
go

--while break continue
WHILE (SELECT AVG(ListPrice) FROM Production.Product) < $300  
BEGIN  
   UPDATE Production.Product  
      SET ListPrice = ListPrice * 2  
   SELECT MAX(ListPrice) FROM Production.Product  
   IF (SELECT MAX(ListPrice) FROM Production.Product) > $500  
      BREAK  
   ELSE  
      CONTINUE  
END  
PRINT 'Too much for the market to bear';  

--goto
DECLARE @Counter int;  
SET @Counter = 1;  
WHILE @Counter < 10  
BEGIN   
    SELECT @Counter  
    SET @Counter = @Counter + 1  
    IF @Counter = 4 GOTO Branch_One --Jumps to the first branch.  
    IF @Counter = 5 GOTO Branch_Two  --This will never execute.  
END  
Branch_One:  
    SELECT 'Jumping To Branch One.'  
    GOTO Branch_Three; --This will prevent Branch_Two from executing.  
Branch_Two:  
    SELECT 'Jumping To Branch Two.'  
Branch_Three:  
    SELECT 'Jumping To Branch Three.';  

--return 


--case when
SELECT   ProductNumber, Name, Price_Range =   
      CASE   
         WHEN ListPrice =  0 THEN 'Mfg item - not for resale'  
         WHEN ListPrice < 50 THEN 'Under $50'  
         WHEN ListPrice >= 50 and ListPrice < 250 THEN 'Under $250'  
         WHEN ListPrice >= 250 and ListPrice < 1000 THEN 'Under $1000'  
         ELSE 'Over $1000'  
      END  
FROM Product  
ORDER BY ProductNumber ;

--waitfor
begin
waitfor delay '02:00';
exec usp_bivariate @tbl='aisles';
end

begin 
waitfor time '10:20';
exec xxxxxe
end

--try catch
begin try 
select 1/0
end try
begin catch
select 1/1
end catch

--throw
USE tempdb;  
GO  
CREATE TABLE dbo.TestRethrow  
(    ID INT PRIMARY KEY  
);  
BEGIN TRY  
    INSERT dbo.TestRethrow(ID) VALUES(1);  
--  Force error 2627, Violation of PRIMARY KEY constraint to be raised.  
    INSERT dbo.TestRethrow(ID) VALUES(1);  
END TRY  
BEGIN CATCH  

    PRINT 'In catch block.';  
    THROW;  
END CATCH;  

--create a function
create function log1p(@input float)
returns float
as
begin
return @input
end

--create trigger



--rank

exec 