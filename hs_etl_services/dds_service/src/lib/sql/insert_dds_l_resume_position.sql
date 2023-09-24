INSERT INTO dds.l_resume_position (
    hk_l_resume_position,
    hk_resume_id,
    hk_position_id,
    load_dt
)
VALUES (
    MD5(CONCAT('%(hk_resume_id)s', '%(hk_position_id)s')),
    %(hk_resume_id)s,
    %(hk_position_id)s,
    NOW()
)
