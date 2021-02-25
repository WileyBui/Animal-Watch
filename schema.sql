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
	category int
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

INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time) VALUES (1, 1, 'Wileys lion text - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTUkwe-Ws_DAXRW-ApsE2ZrAZTSQEkGnSGhCg&usqp=CAU', now());
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time) VALUES (2, 2, 'Allys tiger text - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. ', 'https://images.theconversation.com/files/330851/original/file-20200427-145560-1nlgr5h.jpg', now());
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time) VALUES (3, 3, 'Jakobs elephant text - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://assets.nrdc.org/sites/default/files/styles/full_content--retina/public/media-uploads/wlds43_654640_2400.jpg?itok=LbhnLIk9', now());
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time) VALUES (4, 4, 'Elises snake text - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://thewhiskerchronicles.files.wordpress.com/2014/02/664px-eastern_indigo_snake.jpg', now());
INSERT INTO Posts (users_id, animal_id, post_text, imageURL, post_time) VALUES (5, 5, 'Rays orangutan text - Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 'https://static.scientificamerican.com/blogs/cache/file/65367319-B08B-4C77-8A2F42A5E05C8B53_source.jpg', now());

