INSERT INTO dds.h_technology (
    hk_tech_id,
    tech_id,
    tech_name,
    load_dt
)
SELECT
    MD5((tech_id)::text) as hk_tech_id,
    tech_id,
    tech_name,
    NOW() as load_dt
FROM stg.technologies
ON CONFLICT (hk_tech_id) DO UPDATE
SET
    tech_name = EXCLUDED.tech_name;
