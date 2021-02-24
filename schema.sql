drop table Users CASCADE;
drop table Tags CASCADE;
drop table Animals CASCADE;
drop table Posts CASCADE;
drop table Comments;

create table Users (
	id SERIAL PRIMARY KEY,
	name varchar(255)
);

create table Tags (
	id SERIAL PRIMARY KEY,
	tag varchar(255),
	hexcolor varchar(7)
);

create table Animals (
	id SERIAL PRIMARY KEY,
	name varchar(255),
	endangerment_level int,
	imageURL varchar(255),
	category int,
	tag_id int references Tags
);

create table Posts (
	id SERIAL PRIMARY KEY,
	user_id int references Users,
	animal_id int references Animals,
	text varchar(255),
	location varchar(255),
	imageURL varchar(255),
	lat decimal(20,17),
	long decimal(20,17),
	timestamp time
);

create table Comments (
	id SERIAL PRIMARY KEY,
	user_id int references Users,
	post_id int references Posts,
	text varchar(255),
	timestamp time
);