SELECT
	CASE
		WHEN MAX(load_dt) IS NULL THEN make_timestamp(2000, 1, 1, 0, 0, 0)
		ELSE MAX(load_dt)
	END load_dt
FROM dds.l_position_technology;
