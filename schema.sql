drop table Users;
drop table Tags;
drop table Animals;
drop table Posts;
drop table Comments;
drop table MapContents;

create table Users (
	id SERIAL PRIMARY KEY,
	name varchar(255)
);

create table Tags (
	id SERIAL PRIMARY KEY,
	tag varchar(255)
);

create table Animals (
	id SERIAL PRIMARY KEY,
	name varchar(255),
	endangerment_level int,
	category int,
	tag_id int references Tags
);

create table Posts (
	id SERIAL PRIMARY KEY,
	user_id int references Users,
	animal_id int references Aniimals,
	text varchar(255),
	timestamp time
);

create table Comments (
	id SERIAL PRIMARY KEY,
	user_id int references Users,
	comment_id int references Comments,
	text varchar(255),
	timestamp time
);

create table MapContents (
	id SERIAL PRIMARY KEY,
	-- user_id int references Users,
	-- REFERENCING THE ANIMAL
	latitude	Decimal(20,17),
	longtitude	Decimal(19,17)
);