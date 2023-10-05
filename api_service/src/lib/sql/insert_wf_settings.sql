INSERT INTO stg.wf_settings (
     wf_table,
     wf_key,
     wf_value
)
VALUES (
    %(wf_table)s,
    %(wf_key)s,
    %(wf_value)s
)
ON CONFLICT (wf_table, wf_key) DO UPDATE
SET
    wf_value = EXCLUDED.wf_value;
