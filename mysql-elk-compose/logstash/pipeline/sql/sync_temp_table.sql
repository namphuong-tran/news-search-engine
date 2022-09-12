SELECT *, modification_time AS ts FROM temp_db.es_table
WHERE modification_time > :sql_last_value AND modification_time < NOW()
ORDER BY publish_date