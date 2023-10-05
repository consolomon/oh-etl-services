
INSERT INTO dds.s_position_info (
    hk_position_id,
    position_id,
    position_name,
    position_keywords
)
SELECT
    MD5((position_id)::text) as hk_position_id,
    position_id,
    position_name,
    position_keywords
FROM stg.positions
ON CONFLICT (hk_position_id) DO UPDATE
SET
    position_name = EXCLUDED.position_name,
    position_keywords = EXCLUDED.position_keywords
