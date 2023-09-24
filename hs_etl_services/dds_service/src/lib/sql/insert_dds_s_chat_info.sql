INSERT INTO dds.s_chat_info (
    hk_chat_id,
    chat_id,
    chat_type,
    chat_name,
    title,
    description,
    invite_link,
    members_count,
    is_verified
)
SELECT
    MD5((chat_id)::text) as hk_chat_id,
    chat_id,
    chat_type,
    chat_name,
    title,
    description,
    invite_link,
    members_count,
    is_verified
FROM stg.chats
WHERE
    is_fake IS FALSE AND
    is_scam IS FALSE
ON CONFLICT (hk_chat_id) DO UPDATE
SET
    chat_type = EXCLUDED.chat_type,
    chat_name = EXCLUDED.chat_name,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    invite_link = EXCLUDED.invite_link,
    members_count = EXCLUDED.members_count,
    is_verified = EXCLUDED.is_verified;
