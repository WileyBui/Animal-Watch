drop table Users CASCADE;
drop table Tags CASCADE;
drop table Animals CASCADE;
drop table HasTag;
drop table Locations;
drop table Posts CASCADE;
drop table Comments;
drop table Likes;

create table Users (
	id SERIAL PRIMARY KEY,
	users_name varchar(255)
);

create table Tags (
	id SERIAL PRIMARY KEY,
	tag varchar(255),
	tag_bootstrap_color varchar(255)
);

create table Animals (
	id SERIAL PRIMARY KEY,
	species varchar(255),
	endangerment_level int,
	imageURL varchar(255),
	category int,
	tag_id int references Tags
);

create table HasTag (
	id SERIAL PRIMARY KEY,
	animal_id int references Animals,
	tag_id int references Tags
);

create table Locations (
	id SERIAL PRIMARY KEY,
	users_id int references Users,
	animal_id int references Animals,
	lat decimal(20,17),
	long decimal(20,17)
);

create table Posts (
	id SERIAL PRIMARY KEY,
	users_id int references Users NOT NULL,
	animal_id int references Animals NOT NULL,
	post_text varchar(255),
	imageURL varchar(255),
	post_time timestamp
);

create table Comments (
	id SERIAL PRIMARY KEY,
	users_id int references Users NOT NULL,
	post_id int references Posts NOT NULL,
	comm_text varchar(255),
	comm_time timestamp
);

CREATE TYPE comm_post_t AS ENUM('comment','post');

create table Likes (
	id SERIAL PRIMARY KEY,
	users_id int references Users,
	post_id int references Posts,
	comment_id int references Comments,
	comm_post_type comm_post_t
);