drop table if exists dataset;
create table dataset (
  id integer primary key autoincrement,
  filepath string not null,
  label0y int not null default 0,
  label0n int not null default 0,
  label1y int not null default 0,
  label1n int not null default 0,
  label2y int not null default 0,
  label2n int not null default 0,
  label3y int not null default 0,
  label3n int not null default 0,
  label4y int not null default 0,
  label4n int not null default 0
);