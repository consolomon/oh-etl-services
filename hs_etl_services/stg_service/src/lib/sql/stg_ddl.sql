CREATE SCHEMA IF NOT EXISTS stg AUTHORIZATION postgres;

CREATE TABLE IF NOT EXISTS stg.messages (
	message_id integer NOT NULL,
	message_link varchar NOT NULL,
	from_chat bigint NOT NULL,
	sender_chat bigint NULL,
	sender_user bigint NULL,
	message_ts timestamp NOT NULL,
	views_count integer NULL,
	forwards_count integer NULL,
	message_text varchar NULL,
	attached_user varchar NULL,
	attached_github varchar NULL,
	attached_linkedin varchar NULL,
	attached_link varchar NULL,
	attached_email varchar NULL,
	attached_hashtags varchar NULL
);

CREATE TABLE IF NOT EXISTS stg.chats (
	chat_id bigint NOT NULL,
	chat_type varchar NOT NULL,
	chat_name varchar NOT NULL,
	title varchar NOT NULL,
	description varchar NULL,
	invite_link varchar NULL,
	members_count integer NULL,
	is_verified boolean NULL,
	is_scam boolean NULL,
	is_fake boolean NULL,
	PRIMARY KEY(chat_id)
);

CREATE TABLE IF NOT EXISTS stg.positions (
	position_id serial,
	position_name varchar NOT NULL,
	position_keywords varchar NOT NULL,
	PRIMARY KEY(position_name)
);

CREATE TABLE IF NOT EXISTS stg.technologies (
    tech_id serial,
    tech_name varchar NOT NULL,
    PRIMARY KEY(tech_name)
)

CREATE TABLE IF NOT EXISTS stg.wf_settings (
    wf_id serial,
    wf_table varchar NOT NULL,
    wf_key varchar NOT NULL,
    wf_value varchar NOT NULL,
    PRIMARY KEY(wf_table, wf_key)
)
