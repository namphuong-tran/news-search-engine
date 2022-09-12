-- SELECT *, update_time AS ts FROM temp_db.temp_table
-- WHERE update_time > :sql_last_value AND update_time < NOW()
-- ORDER BY id


SELECT *, modification_time AS ts FROM temp_db.es_table
WHERE modification_time > :sql_last_value AND modification_time < NOW()
ORDER BY publish_date