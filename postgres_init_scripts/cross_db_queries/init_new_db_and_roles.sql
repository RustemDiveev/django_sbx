-- Выполнять под пользователем postgres 

create user alice password 'alice';
create user bob password 'bob';

create database alice_db with owner = 'alice';
create database bob_db with owner = 'bob';