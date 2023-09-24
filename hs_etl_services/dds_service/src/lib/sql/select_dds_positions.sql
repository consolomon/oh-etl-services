SELECT
    hp.hk_position_id,
    spi.position_keywords
FROM dds.h_position AS hp
LEFT JOIN dds.s_position_info AS spi
ON hp.hk_position_id = spi.hk_position_id
