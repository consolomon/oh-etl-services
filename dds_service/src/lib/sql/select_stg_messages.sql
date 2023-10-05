SELECT DISTINCT ON (M.message_ts, M.from_chat) *
FROM stg.messages as M
WHERE
    M.message_ts > %(message_ts)s AND
    M.message_text IS NOT NULL
ORDER BY M.message_ts ASC
LIMIT %(batch_limit)s;
