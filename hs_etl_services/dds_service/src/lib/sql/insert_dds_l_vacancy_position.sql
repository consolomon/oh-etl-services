INSERT INTO dds.l_vacancy_position (
    hk_l_vacancy_position,
    hk_vacancy_id,
    hk_position_id,
    load_dt
)
VALUES (
    MD5(CONCAT('%(hk_vacancy_id)s', '%(hk_position_id)s')),
    %(hk_vacancy_id)s,
    %(hk_position_id)s,
    NOW()
)
