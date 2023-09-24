SELECT
	hv.hk_vacancy_id,
	hv.load_dt,
	svi.message_text
FROM dds.h_vacancy AS hv
LEFT JOIN dds.s_vacancy_info AS svi
ON hv.hk_vacancy_id = svi.hk_vacancy_id
WHERE hv.load_dt > %(load_dt)s
ORDER BY hv.load_dt ASC
LIMIT %(batch_limit)s;
