drop table if exists challenger
create table challenger (O_Ring_Failure char(1),
Launch_temperature float,
Leak_check_pressure char(10))

select * from challenger
insert into challenger values ('N',66,'Low')
insert into challenger values ('N',69,'Low')
insert into challenger values ('N',68,'Low')
insert into challenger values ('N',67,'Low')
insert into challenger values ('N',72,'Low')
insert into challenger values ('N',73,'Low')
insert into challenger values ('N',70,'Low')
insert into challenger values ('N',78,'High')
insert into challenger values ('N',67,'High')
insert into challenger values ('N',67,'High')
insert into challenger values ('N',75,'High')
insert into challenger values ('N',70,'High')
insert into challenger values ('N',81,'High')
insert into challenger values ('N',76,'High')
insert into challenger values ('N',79,'High')
insert into challenger values ('N',75,'High')
insert into challenger values ('N',76,'High')
insert into challenger values ('Y',70,'Low')
insert into challenger values ('Y',57,'High')
insert into challenger values ('Y',63,'High')
insert into challenger values ('Y',70,'High')
insert into challenger values ('Y',53,'High')
insert into challenger values ('Y',58,'High')
go

select * from challenger
go

alter table challenger add 
	Y_temperature float,
	N_temperature float;
go

with cte1
as
( select Launch_temperature  as y_temp from challenger where O_Ring_Failure='Y'),
cte2 as(select Launch_temperature  as n_temp from challenger where O_Ring_Failure='N')

insert into challenger 
	select y_temp， n_temp from cte1, cte2;
go
select * from challenger