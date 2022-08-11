-- postgres (postgres)
CREATE DATABASE alice_db;
CREATE DATABASE bob_db;
CREATE DATABASE carl_db;

CREATE USER alice PASSWORD 'alice';
CREATE USER bob PASSWORD 'bob';
CREATE USER carl PASSWORD 'carl';

-- что интересно, alice спокойно может подключиться к alice_db и создать там таблицу, например 
-- нам нужно сделать так, чтобы каждый пользователь мог ходить только в свою бд 

-- чтобы ни один пользователь не мог подключиться к только что созданным БД 
REVOKE CONNECT ON DATABASE alice_db FROM PUBLIC; 
REVOKE CONNECT ON DATABASE bob_db FROM PUBLIC; 
REVOKE CONNECT ON DATABASE carl_db FROM PUBLIC; 

-- Назначаем владельцев БД - теперь они могут подключаться к ней (каждый к своей) и создавать объекты 
ALTER DATABASE alice_db OWNER TO alice;
ALTER DATABASE bob_db OWNER TO bob;
ALTER DATABASE carl_db OWNER TO carl;

-- postgres (postgres)
-- Создаем специального пользователя только на чтение
CREATE USER bob_readonly PASSWORD 'bob_readonly';
GRANT CONNECT ON DATABASE bob_db TO bob_readonly;

-- bob_readonly в bob_db может создавать объекты, его надо лишить этой возможности 
-- https://stackoverflow.com/questions/760210/how-do-you-create-a-read-only-user-in-postgresql/39029296#39029296
-- https://stackoverflow.com/questions/49206699/postgres-revoke-database-access-from-user

-- сработало следующее, но надо быть осторожным 
-- bob_db (diveevri)
-- мы должны вернуть права на создание владельцу БД
REVOKE CREATE ON SCHEMA public from public;
GRANT CREATE ON SCHEMA public to bob;

-- выдаю права на чтение всех таблиц 

-- вот это не сработало ни под bob, ни под diveevri
-- grant pg_read_all_data to bob_readonly;

-- bob_db (diveevri)
grant select on all tables in schema public to bob_readonly;
-- но это не решение - пользователь не видит новых таблиц 

-- нужно обязательно выполнить это под тем пользователем, что будет создавать объекты 
-- в моем случае это bob_db (bob)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO bob_readonly;

-- postgres (postgres)
CREATE USER alice_postprocess PASSWORD 'alice_postprocess';
GRANT CONNECT ON DATABASE alice_db TO alice_postprocess;

-- пользователь alice_postprocess должен уметь подключаться только к alice_db, +

-- не может удалять существующие и создавать новые таблицы
-- может изменять данные в существующих таблицах 
-- может создавать процедуры / функции 
-- alice_db (diveevri)
REVOKE CREATE ON SCHEMA public FROM public;
GRANT CREATE ON SCHEMA public TO alice;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO alice_postprocess;

-- alice_db(alice)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO alice_postprocess;

-- Ситуация следующая - нельзя давать пользователю создавать новые и удалять существующие объекты 
-- это сделать удалось, но для создания функций и процедур нужна привилегия на create 
-- а мы её отозвали ранее 
-- поэтому придется создать новую схему - в которой дать пользователю привилегию на создание 

-- alice_db (diveevri)
create schema pp;
grant create on schema pp to alice_postprocess;
-- вот сейчас круто - создавать могу, но не могу дропать и выполнять 
GRANT USAGE ON SCHEMA pp TO alice_postprocess;
-- сейчас типи топ, могу читать из public, могу создавать и выполнять процедуры и функции в схеме pp

-- часть, связанная с созданием внешних таблиц и использованием foreign data wrapper 
-- пока все делаю под суперпользователем 
-- alice_db (diveevri)
CREATE EXTENSION postgres_fdw;

CREATE SERVER bob_server 
FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    host 'localhost',
    port '5432',
    dbname 'bob_db'
);

-- нужно, чтобы alice_postprocess могла читать из внешних таблиц
CREATE USER MAPPING FOR alice_postprocess SERVER bob_server OPTIONS (
    user 'bob_readonly', password 'bob_readonly'
);

-- нужно, чтобы owner бд мог создавать внешние таблицы 
-- при каждом создании таблиц в public.alice_db 
CREATE USER MAPPING FOR alice SERVER bob_server OPTIONS (
    user 'bob_readonly', password 'bob_readonly'
);

-- create foreign table необходимо выполнять не под суперпользователем 
-- alice_db (alice)
/*
create foreign table bob_test (
    id integer
) 
server bob_server options (
    schema_name 'public',
    table_name 'bob_test'
);
*/

-- alice_db (diveevri)
GRANT USAGE ON FOREIGN SERVER bob_server TO alice;

-- теперь foreign table создается 
-- УРА!

-- если удалить bob_test в bob_db или в alice_db 
-- то процедура будет падать с ошибкой
-- но если все вернуть, то работает 
-- поэтому можно пересоздавать внешние таблицы и не трогать процедуры
-- простейший способ 
DROP FOREIGN TABLE bob_test;
IMPORT FOREIGN SCHEMA public LIMIT TO (bob_test)
    FROM SERVER bob_server INTO public;