SELECT
     wf_id,
     wf_table,
     wf_key,
     wf_value
FROM stg.wf_settings
WHERE
    wf_table = %(wf_table)s AND
    wf_key = %(wf_key)s;
