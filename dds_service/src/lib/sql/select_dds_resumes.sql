SELECT
	hr.hk_resume_id,
	hr.load_dt,
	sri.message_text
FROM dds.h_resume AS hr
LEFT JOIN dds.s_resume_info AS sri
ON hr.hk_resume_id = sri.hk_resume_id
WHERE hr.load_dt > %(load_dt)s
ORDER BY hr.load_dt ASC
LIMIT %(batch_limit)s;
