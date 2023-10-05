INSERT INTO dds.l_position_technology (
	hk_l_position_technology,
	hk_position_id,
	hk_tech_id,
	load_dt
)
SELECT
    MD5(CONCAT(PT.hk_position_id, PT.hk_tech_id)) AS hk_l_position_technology,
    PT.hk_position_id,
    PT.hk_tech_id,
    NOW() AS load_dt
FROM (
	SELECT
		lvp.hk_position_id AS hk_position_id,
		lvt.hk_tech_id AS hk_tech_id
	FROM dds.l_vacancy_position AS lvp
	JOIN dds.l_vacancy_technology AS lvt
	ON lvp.hk_vacancy_id = lvt.hk_vacancy_id
	WHERE lvt.load_dt > %(load_dt)s
	UNION
	SELECT
		lrp.hk_position_id AS hk_position_id,
		lrt.hk_tech_id AS hk_tech_id
	FROM dds.l_resume_position AS lrp
	JOIN dds.l_resume_technology AS lrt
	ON lrp.hk_resume_id = lrt.hk_resume_id
	WHERE lrt.load_dt > %(load_dt)s
) AS PT
WHERE
	MD5(CONCAT(PT.hk_position_id, PT.hk_tech_id)) NOT IN (
		SELECT
			hk_l_position_technology
		FROM dds.l_position_technology
	);
