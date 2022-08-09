/*
    https://stackoverflow.com/questions/46324/possible-to-perform-cross-database-queries-with-postgresql
    Выделяют два способа: 
        1) через foreign data wrapper - актуальнее чем второй 
            https://www.postgresql.org/docs/current/postgres-fdw.html
        2) через dblink 
            https://www.postgresql.org/docs/current/dblink.html
*/

/*
    Этапы подготовки согласно документации: 

    Foreign Data Wrapper 
    1. Install the postgres_fdw extension using CREATE EXTENSION.

    2. Create a foreign server object, using CREATE SERVER, to represent each remote database you want to connect to. 
    Specify connection information, except user and password, as options of the server object.

    3. Create a user mapping, using CREATE USER MAPPING, 
    for each database user you want to allow to access each foreign server. 
    Specify the remote user name and password to use as user and password options of the user mapping.

    4. Create a foreign table, using CREATE FOREIGN TABLE or IMPORT FOREIGN SCHEMA, 
    for each remote table you want to access. 
    The columns of the foreign table must match the referenced remote table. 
    You can, however, use table and/or column names different from the remote table's, 
    if you specify the correct remote names as options of the foreign table object.
*/

/*
    Нюансы:
    1. Расширение устанавливается на уровне БД
*/

-- нужен суперпользователь (diveevri) в alice_db, bob_db
CREATE EXTENSION postgres_fdw;

-- можно сделать под обычным пользователем, если есть привилегия usage на extension - далее делать все под alice например
/*
CREATE SERVER foreign_server
FOREIGN DATA WRAPPER postgres_fdw
OPTIONS (host '192.83.123.89', port '5432', dbname 'foreign_db');
*/

-- alice_db (diveevri)
CREATE SERVER bob_server 
FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    host 'localhost', 
    port '5432',
    dbname 'bob_db'
);

-- bob_db (diveevri) - TBD 

-- alice_db (diveevri)
CREATE USER MAPPING FOR alice SERVER bob_server OPTIONS (
    user 'bob', password 'bob'
);


CREATE FOREIGN TABLE foreign_bob_table (
        id integer
)
SERVER bob_server
OPTIONS (
    schema_name 'public', 
    table_name 'bob_table'
);

GRANT SELECT ON foreign_bob_table TO alice;

/*
    -- alice_db (alice)
    select * from foreign_bob_table
*/

/*
    Далее - пример через dblink 
*/

-- alice_db (diveevri)
CREATE EXTENSION dblink;

-- внимание, нужно явно указывать public 
SELECT *
    FROM dblink('hostaddr=127.0.0.1 port=5432 dbname=bob_db user=bob password=bob options=-csearch_path= ',
                'select id from public.bob_table')
      AS t1(id integer);

-- Можно явно сохранить подключение отдельно, а затем пользоваться им по имени: 
-- https://www.postgresql.org/docs/current/contrib-dblink-connect.html