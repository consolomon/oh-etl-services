INSERT INTO dds.h_chat (
    hk_chat_id,
    chat_id,
    load_dt
)
SELECT
    MD5((chat_id)::text) as hk_chat_id,
    chat_id,
    now() as load_dt
FROM stg.chats
WHERE
    is_fake IS FALSE AND
    is_scam IS FALSE
ON CONFLICT (hk_chat_id) DO NOTHING;
