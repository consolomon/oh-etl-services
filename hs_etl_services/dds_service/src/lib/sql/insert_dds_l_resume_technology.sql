INSERT INTO dds.l_resume_technology (
    hk_l_resume_technology,
    hk_resume_id,
    hk_tech_id,
    load_dt
)
VALUES (
    MD5(CONCAT('%(hk_resume_id)s', '%(hk_tech_id)s')),
    %(hk_resume_id)s,
    %(hk_tech_id)s,
    NOW()
)
