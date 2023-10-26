SELECT
	C.chat_name,
	MIN(M.message_ts) AS first_msg_ts,
	MAX(M.message_ts) AS last_msg_ts,
	COUNT(*) AS msg_count
FROM stg.messages AS M
LEFT JOIN stg.chats AS C
ON M.from_chat = C.chat_id
GROUP BY C.chat_id;
