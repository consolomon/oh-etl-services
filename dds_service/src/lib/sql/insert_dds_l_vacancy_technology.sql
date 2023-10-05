INSERT INTO dds.l_vacancy_technology (
    hk_l_vacancy_technology,
    hk_vacancy_id,
    hk_tech_id,
    load_dt
)
VALUES (
    MD5(CONCAT('{hk_vacancy_id}', '{hk_tech_id}')),
    '{hk_vacancy_id}',
    '{hk_tech_id}',
    NOW()
)
ON CONFLICT (hk_l_vacancy_technology) DO NOTHING;
