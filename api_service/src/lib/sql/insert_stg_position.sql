INSERT INTO stg.positions (
    position_name,
    position_keywords
)
VALUES (
    %(position_name)s,
    %(position_keywords)s
)
ON CONFLICT (position_name) DO UPDATE
SET
    position_keywords = EXCLUDED.position_keywords;
