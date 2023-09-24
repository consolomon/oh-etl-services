INSERT INTO dds.h_position (
    hk_position_id,
    position_id,
    load_dt
)
SELECT
    MD5((position_id)::text) as hk_position_id,
    position_id,
    NOW() as load_dt
FROM stg.positions
ON CONFLICT (hk_position_id) DO NOTHING;
