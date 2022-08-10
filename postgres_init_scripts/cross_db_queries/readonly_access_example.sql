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

/*
    TODO:
    1. Необходимо зарегистрировать пользователя alice_postprocess с подключением только к alice_db 
    2. Необходимо сделать так, чтобы alice_postprocess был натравлен на bob_db 
    3. Необходимо сделать так, чтобы alice_postprocess мог как создавать процедуры, так и читать из внешних таблиц, так и читать из таблиц public.
*/