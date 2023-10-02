INSERT INTO dds.l_vacancy_position (
    hk_l_vacancy_position,
    hk_vacancy_id,
    hk_position_id,
    load_dt
)
VALUES (
    MD5(CONCAT('{hk_vacancy_id}', '{hk_position_id}')),
    '{hk_vacancy_id}',
    '{hk_position_id}',
    NOW()
)
ON CONFLICT (hk_l_vacancy_position) DO NOTHING;
