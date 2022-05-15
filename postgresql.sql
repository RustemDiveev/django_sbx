create user django_tech_user with password 'EZheFinzl';
create database django_sbx;
grant all on database django_sbx to django_tech_user;

/*Нужно для запуска тестов, так как создается временная отдельная БД*/
alter user django_tech_user createdb;