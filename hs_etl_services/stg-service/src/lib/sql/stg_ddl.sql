CREATE TABLE IF NOT EXISTS stg.messages (
	message_id integer NOT NULL,
	from_chat json NOT NULL,
	from_user json NULL,
	message_ts timestamp NOT NULL,
	link varchar NOT NULL,
	views_count integer NULL,
	forwards_count integer NULL,
	message_text varchar NULL,
	entities_list varchar NULL
);

CREATE TABLE IF NOT EXISTS stg.chats (
	chat_id integer NOT NULL,
	chat_type varchar NOT NULL,
	title varchar NOT NULL,
	description varchar NULL,
	invite_link varchar NULL,
	members_count integer NULL,
	restrictions_list varchar NULL,
	is_verified boolean NULL,
	is_scum boolean NULL,
	is_fake boolean NULL
);

CREATE TABLE IF NOT EXISTS stg.positions (
	position_id serial,
	position_name varchar,
	position_keywords varchar
);
