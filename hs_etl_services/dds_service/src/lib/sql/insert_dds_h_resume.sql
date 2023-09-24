INSERT INTO dds.h_resume (
    hk_resume_id,
	chat_id,
	message_id,
	load_dt
)
VALUES (
    MD5(CONCAT(%(chat_id)s, %(message_id)s)),
    %(chat_id)s,
    %(message_id)s,
    now()
);
