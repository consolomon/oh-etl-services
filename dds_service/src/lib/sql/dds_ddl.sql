CREATE SCHEMA IF NOT EXISTS dds AUTHORIZATION postgres;

CREATE TABLE IF NOT EXISTS dds.h_chat (
	hk_chat_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_chat_id)
);

CREATE TABLE IF NOT EXISTS dds.h_position (
	hk_position_id varchar NOT NULL,
	position_id integer NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_position_id)
);

CREATE TABLE IF NOT EXISTS dds.h_technology (
	hk_tech_id varchar NOT NULL,
	tech_id integer NOT NULL,
	tech_name varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_tech_id)
);

CREATE TABLE IF NOT EXISTS dds.h_vacancy (
	hk_vacancy_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	message_id integer NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_vacancy_id)
);

CREATE TABLE IF NOT EXISTS dds.h_resume (
	hk_resume_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	message_id integer NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_resume_id)
);

CREATE TABLE IF NOT EXISTS dds.s_vacancy_info (
	hk_vacancy_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	message_id integer NOT NULL,
	message_link varchar NOT NULL,
	sender_chat bigint NULL,
	sender_user bigint NULL,
	message_ts timestamp NOT NULL,
	views_count integer NULL,
	forwards_count integer NULL,
	message_text varchar NULL,
	attached_user varchar NULL,
	attached_link varchar NULL,
	attached_email varchar NULL,
	attached_hashtags varchar NULL,
	work_experience varchar NULL,
	grade varchar NULL,
	work_format varchar NULL,
	PRIMARY KEY(hk_vacancy_id)
);

CREATE TABLE IF NOT EXISTS dds.s_resume_info (
	hk_resume_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	message_id integer NOT NULL,
	message_link varchar NOT NULL,
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
	attached_hashtags varchar NULL,
	work_experience varchar NULL,
	grade varchar NULL,
	work_format varchar NULL,
	PRIMARY KEY(hk_resume_id)
);

CREATE TABLE IF NOT EXISTS dds.s_chat_info (
	hk_chat_id varchar NOT NULL,
	chat_id bigint NOT NULL,
	chat_type varchar NOT NULL,
	chat_name varchar NOT NULL,
	title varchar NOT NULL,
	description varchar NULL,
	invite_link varchar NULL,
	members_count integer NULL,
	is_verified boolean NULL,
	PRIMARY KEY(hk_chat_id)
);

CREATE TABLE IF NOT EXISTS dds.s_position_info (
	hk_position_id varchar NOT NULL,
	position_id integer NOT NULL,
	position_name varchar NOT NULL,
	position_keywords varchar NOT NULL,
	PRIMARY KEY(hk_position_id)
);

CREATE TABLE IF NOT EXISTS dds.l_vacancy_position (
    hk_l_vacancy_position varchar NOT NULL,
    hk_vacancy_id varchar NOT NULL,
    hk_position_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_l_vacancy_position),
	FOREIGN KEY(hk_position_id) REFERENCES dds.h_position(hk_position_id),
	FOREIGN KEY(hk_vacancy_id) REFERENCES dds.h_vacancy(hk_vacancy_id)
);

CREATE TABLE IF NOT EXISTS dds.l_vacancy_technology (
    hk_l_vacancy_technology varchar NOT NULL,
    hk_vacancy_id varchar NOT NULL,
    hk_tech_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_l_vacancy_technology),
	FOREIGN KEY(hk_tech_id) REFERENCES dds.h_technology(hk_tech_id),
	FOREIGN KEY(hk_vacancy_id) REFERENCES dds.h_vacancy(hk_vacancy_id)
);

CREATE TABLE IF NOT EXISTS dds.l_resume_position (
    hk_l_resume_position varchar NOT NULL,
    hk_resume_id varchar NOT NULL,
    hk_position_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_l_resume_position),
	FOREIGN KEY(hk_position_id) REFERENCES dds.h_position(hk_position_id),
	FOREIGN KEY(hk_resume_id) REFERENCES dds.h_resume(hk_resume_id)
);

CREATE TABLE IF NOT EXISTS dds.l_resume_technology (
    hk_l_resume_technology varchar NOT NULL,
    hk_resume_id varchar NOT NULL,
    hk_tech_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_l_resume_technology),
	FOREIGN KEY(hk_tech_id) REFERENCES dds.h_technology(hk_tech_id),
	FOREIGN KEY(hk_resume_id) REFERENCES dds.h_resume(hk_resume_id)
);

CREATE TABLE IF NOT EXISTS dds.l_position_technology (
    hk_l_position_technology varchar NOT NULL,
    hk_position_id varchar NOT NULL,
    hk_tech_id varchar NOT NULL,
	load_dt timestamp NOT NULL,
	PRIMARY KEY(hk_l_position_technology),
	FOREIGN KEY(hk_position_id) REFERENCES dds.h_position(hk_position_id),
	FOREIGN KEY(hk_tech_id) REFERENCES dds.h_technology(hk_tech_id)
);

CREATE TABLE IF NOT EXISTS dds.wf_settings (
    wf_id serial,
    wf_table varchar NOT NULL,
    wf_key varchar NOT NULL,
    wf_value varchar NOT NULL,
    PRIMARY KEY(wf_table, wf_key)
)
