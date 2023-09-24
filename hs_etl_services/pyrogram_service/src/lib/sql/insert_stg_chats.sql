INSERT INTO stg.chats (
    chat_id,
    chat_type,
    chat_name,
    title,
    description,
    invite_link,
    members_count,
    is_verified,
    is_scam,
    is_fake
)
VALUES (
    %(chat_id)s,
    %(chat_type)s,
    %(chat_name)s,
    %(title)s,
    %(description)s,
    %(invite_link)s,
    %(members_count)s,
    %(is_verified)s,
    %(is_scam)s,
    %(is_fake)s
)
ON CONFLICT (chat_id) DO UPDATE
SET
    chat_type = EXCLUDED.chat_type,
    chat_name = EXCLUDED.chat_name,
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    invite_link = EXCLUDED.invite_link,
    members_count = EXCLUDED.members_count,
    is_verified = EXCLUDED.is_verified,
    is_scam = EXCLUDED.is_scam,
    is_fake = EXCLUDED.is_fake;
