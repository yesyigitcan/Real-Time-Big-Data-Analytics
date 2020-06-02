create view inf_20 as (select * from inf where profile_id = 20);

create or replace view inf_20_4
as (select * from inf_20
where mod(id,4) = 0);

create or replace view inf_20_2
as (select * from inf_20
where mod(id,2) = 0);