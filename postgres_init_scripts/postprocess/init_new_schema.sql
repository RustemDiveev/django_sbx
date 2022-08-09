-- Выполнять под пользователем sbx_pp 
CREATE SCHEMA catalog_one;
CREATE SCHEMA catalog_two;

-- Выполнять под пользователем postgres 
CREATE USER catalog_one PASSWORD 'catalog_one';
CREATE USER catalog_two PASSWORD 'catalog_two';

