SELECT
	'vacancy' AS post_type,
	COUNT(DISTINCT hv.hk_vacancy_id) as total_count,
	COUNT(
		DISTINCT CASE
			WHEN hk_l_vacancy_position IS NOT NULL THEN hv.hk_vacancy_id
		END
	) AS have_positions,
	COUNT(
		DISTINCT CASE
			WHEN hk_l_vacancy_technology IS NOT NULL THEN hv.hk_vacancy_id
		END
	) AS have_tech
FROM dds.h_vacancy AS hv
LEFT JOIN dds.l_vacancy_technology lvt
ON hv.hk_vacancy_id = lvt.hk_vacancy_id
LEFT JOIN dds.l_vacancy_position AS lvp
ON hv.hk_vacancy_id = lvp.hk_vacancy_id
UNION
SELECT
	'resume' AS post_type,
	COUNT(DISTINCT hr.hk_resume_id) as total_count,
	COUNT(
		DISTINCT CASE
			WHEN hk_l_resume_position IS NOT NULL THEN hr.hk_resume_id
		END
	) AS have_positions,
	COUNT(
		DISTINCT CASE
			WHEN hk_l_resume_technology IS NOT NULL THEN hr.hk_resume_id
		END
	) AS have_tech
FROM dds.h_resume AS hr
LEFT JOIN dds.l_resume_technology AS lrt
ON hr.hk_resume_id = lrt.hk_resume_id
LEFT JOIN dds.l_resume_position AS lrp
ON hr.hk_resume_id = lrp.hk_resume_id;
