INSERT INTO stg.technologies (
    tech_name
)
VALUES (
    %(tech_name)s
)
ON CONFLICT (tech_name) DO NOTHING;
