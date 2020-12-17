drop table in_magazine;
drop table in_pack;
drop table pack;
drop table similar_treat;

-- psql -U ps -d elves_workspace -a -f create.sql

create table in_magazine(
    treat text not null primary key, 
    remaining integer not null, 
    CHECK(remaining >= 0)
);

create table in_pack(
    pack_id integer not null, 
    treat text not null, 
    amount integer not null
);

create table pack(
    id serial primary key, 
    place text not null,
    receiver text not null
);

create table similar_treat(
    treat_1 text, 
    treat_2 text,
    similarity real,
    constraint treat_1_treat_2 primary key(treat_1, treat_2)
);

insert into in_magazine (treat, remaining) values ('zozole', 9999);
insert into in_magazine (treat, remaining) values ('michalki', 9999);
insert into in_magazine (treat, remaining) values ('czekolada gorzka', 9999);
insert into in_magazine (treat, remaining) values ('czekolada mleczna', 9999);
insert into in_magazine (treat, remaining) values ('mietusy', 9999);

insert into similar_treat (treat_1, treat_2, similarity) values ('zozole', 'michalki', 0.5);
insert into similar_treat (treat_1, treat_2, similarity) values ('zozole', 'mietusy', 0.9);
insert into similar_treat (treat_1, treat_2, similarity) values ('mietusy', 'michalki', 0.6);
insert into similar_treat (treat_1, treat_2, similarity) values ('czekolada gorzka', 'czekolada mleczna', 0.7);
insert into similar_treat (treat_1, treat_2, similarity) values ('czekolada gorzka', 'michalki', 0.4);
insert into similar_treat (treat_1, treat_2, similarity) values ('michalki', 'czekolada mleczna', 0.6);
