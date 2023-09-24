SELECT DISTINCT ON (chat_id)
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
FROM stg.chats
