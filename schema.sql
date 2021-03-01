drop table Users CASCADE;
drop table Tags CASCADE;
drop table Animals CASCADE;
drop table HasTag;
drop table Locations;
drop table Posts CASCADE;
drop table Comments CASCADE;
drop table Likes;

create table Users (
	id SERIAL PRIMARY KEY,
	users_name varchar(255),
	profile_picture text
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
	animal_range varchar(255),
	classification varchar(255)
);

-- create table AnimalLikes (
-- 	id SERIAL PRIMARY KEY,
-- 	animal_id int references Animal,
-- 	id_user int references Users
-- )

-- create table HasAnimalLike (
-- 	id SERIAL PRIMARY KEY,
-- 	animal_id int references Animals,
-- 	tag_id int references Tags
-- );

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
	users_id 	INT REFERENCES Users NOT NULL,
	animal_id 	INT REFERENCES Animals NOT NULL,
	post_text 	TEXT NOT NULL,
	imageURL 	TEXT,
	latitude 	DECIMAL(20,17) NOT NULL,
	longitude 	DECIMAL(20,17) NOT NULL,
	post_time 	TIMESTAMP DEFAULT(NOW())
);

create table Comments (
	id SERIAL PRIMARY KEY,
	users_id int references Users NOT NULL,
	animal_id int references Animals NOT NULL,
	comm_text text,
	comm_time TIMESTAMP DEFAULT(NOW())
);

CREATE TYPE comm_post_t AS ENUM('comment','post');

create table Likes (
	id SERIAL PRIMARY KEY,
	users_id int references Users,
	post_id int references Posts,
	comment_id int references Comments,
	comm_post_type comm_post_t
);


INSERT INTO Users (users_name) VALUES ('Wiley Bui');
INSERT INTO Users (users_name) VALUES ('Ally Goins');
INSERT INTO Users (users_name) VALUES ('Jakob Speert');
INSERT INTO Users (users_name) VALUES ('Elise Tran');
INSERT INTO Users (users_name) VALUES ('Ray Lauffer');


INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('needs identification', 'primary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('poisonous animal', 'danger');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('bird', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('#snake', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('#orangutan', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('dangerous animal', 'danger');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('#lion', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('#tiger', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('#elephant', 'secondary');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('cuteness alert', 'success');
INSERT INTO Tags (tag, tag_bootstrap_color) VALUES ('TBU', 'warning');


INSERT INTO Animals (species, endangerment_level, imageURL, category) VALUES ('Small Lion Thing', 10, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUkwe-Ws_DAXRW-ApsE2ZrAZTSQEkGnSGhCg&usqp=CAU', 1);
INSERT INTO Animals (species, endangerment_level, imageURL, category) VALUES ('Small Tiger Thing', 3, 'https://images.theconversation.com/files/330851/original/file-20200427-145560-1nlgr5h.jpg', 2);
INSERT INTO Animals (species, endangerment_level, imageURL, category) VALUES ('Small Elephant Thing', 3, 'https://assets.nrdc.org/sites/default/files/styles/full_content--retina/public/media-uploads/wlds43_654640_2400.jpg?itok=LbhnLIk9', 2);
INSERT INTO Animals (species, endangerment_level, imageURL, category) VALUES ('Small Snake Thing', 5, 'https://thewhiskerchronicles.files.wordpress.com/2014/02/664px-eastern_indigo_snake.jpg', 2);
INSERT INTO Animals (species, endangerment_level, imageURL, category) VALUES ('Small Orangutan Thing', 5, 'https://static.scientificamerican.com/blogs/cache/file/65367319-B08B-4C77-8A2F42A5E05C8B53_source.jpg', 2);


INSERT INTO HasTag (animal_id, tag_id) VALUES (1, 6);
INSERT INTO HasTag (animal_id, tag_id) VALUES (1, 7);
INSERT INTO HasTag (animal_id, tag_id) VALUES (2, 6);
INSERT INTO HasTag (animal_id, tag_id) VALUES (2, 8);
INSERT INTO HasTag (animal_id, tag_id) VALUES (3, 9);
INSERT INTO HasTag (animal_id, tag_id) VALUES (4, 2);
INSERT INTO HasTag (animal_id, tag_id) VALUES (4, 4);
INSERT INTO HasTag (animal_id, tag_id) VALUES (5, 5);
INSERT INTO HasTag (animal_id, tag_id) VALUES (5, 1);

INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (1, 1, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUkwe-Ws_DAXRW-ApsE2ZrAZTSQEkGnSGhCg&usqp=CAU', now(), 44.95572585775119, -92.94149279594421);
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (2, 2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ', 'https://images.theconversation.com/files/330851/original/file-20200427-145560-1nlgr5h.jpg', now(), 45.32382673072401, -93.36995959281921);
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (3, 3, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 'https://assets.nrdc.org/sites/default/files/styles/full_content--retina/public/media-uploads/wlds43_654640_2400.jpg?itok=LbhnLIk9', now(), 45.37787226495894, -92.46908068656921);
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (4, 4, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 'https://thewhiskerchronicles.files.wordpress.com/2014/02/664px-eastern_indigo_snake.jpg', now(), 45.57816100549887, -94.14449572563171);
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (5, 5, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 'https://static.scientificamerican.com/blogs/cache/file/65367319-B08B-4C77-8A2F42A5E05C8B53_source.jpg', now(), 44.322535559213236, -93.26558947563171);
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time, latitude, longitude) VALUES (5, 2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. ', 'https://www.rd.com/wp-content/uploads/2019/04/shutterstock_1013848126.jpg', now(), 44.55002742744211, -95.12227892875671);


INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (5, 1, 'I have a question: Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (4, 2, 'I have a question: Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (3, 3, 'I have a question: Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (2, 4, 'I have a question: Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (1, 5, 'I have a question: Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing industries for previewing layouts and visual mockups.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (1, 1, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (2, 2, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (3, 3, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (4, 4, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (5, 5, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (5, 1, 'Ok that makes sense, thank you!');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (4, 2, 'Ok that makes sense, thank you!');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (3, 3, 'Ok that makes sense, thank you!');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (2, 4, 'Ok that makes sense, thank you!');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (1, 5, 'Ok that makes sense, thank you!');
INSERT INTO COMMENTS (users_id, animal_id, comm_text) VALUES (2, 5, 'Okay this is a test!');
