drop table if exists sports;
drop table if exists items;
create table sports (
    id serial primary key,
    name varchar(50) unique);
create table items (
    id serial primary key,
    cat_id integer,
    title varchar(255) not null,
    description varchar(255));
insert into sports (name) values ('Soccer');
insert into sports (name) values ('Basketball');
insert into sports (name) values ('Baseball');
insert into sports (name) values ('Frisbee');
insert into sports (name) values ('Snowboarding');
insert into items (cat_id, title, description) values (1, 'The shoes', 'Good condition, Reasonalbe price, good quality');
insert into items (cat_id, title, description) values (1, 'The shirt', 'Not good condition, Price is okay, not good condition');
insert into items (cat_id, title, description) values (3, 'The bat', 'condition is so-so, but very expensive');
insert into items (cat_id, title, description) values (5, 'Snowboard', 'Good condition, good quality');
insert into items (cat_id, title, description) values (5, 'Snowboard', 'Bad condition, good quality');
