-- Выполнять под пользователем Postgres:

create role sbx_data_01 login password 'sbx_data_01';
create role sbx_data_stg_01 login password 'sbx_data_stg_01';
create role sbx_pp login password 'sbx_pp';

-- Данные пользовательских объектов
create database sbx_data_01 with owner = sbx_data_01;
-- Предварительные данные пользовательских объектов
create database sbx_data_stg_01 with owner = sbx_data_stg_01;
-- БД, связанная с постпроцессами 
create database sbx_pp with owner = sbx_pp;


