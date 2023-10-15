INSERT INTO dds.h_not_match (
    hk_not_match_id,
	chat_id,
	message_id,
	load_dt
)
VALUES (
    MD5(CONCAT(%(chat_id)s, %(message_id)s)),
    %(chat_id)s,
    %(message_id)s,
    now()
)
ON CONFLICT (hk_not_match_id) DO NOTHING;
