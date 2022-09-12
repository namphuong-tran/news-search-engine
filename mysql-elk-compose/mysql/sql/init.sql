-- USE `temp_db`;
-- DROP TABLE IF EXISTS `es_table`;
-- CREATE TABLE `es_table` (
--   `id` CHAR(36) NOT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY unique_id (`id`),
--   `title` TEXT NOT NULL,
--   `newspaper` VARCHAR(50) NOT NULL,
--   `authors` TEXT,
--   `publish_date` DATETIME, 
--   `keywords` TEXT,
--   `summary` TEXT, 
--   `text` LONGTEXT,
--   `url` VARCHAR(200) NOT NULL,
--   `modification_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );



USE `temp_db`;
DROP TABLE IF EXISTS `es_table`;
CREATE TABLE `es_table` (
  `id` CHAR(36) NOT NULL,
  PRIMARY KEY (`id`, `url`),
  `title` TEXT NOT NULL,
  `newspaper` VARCHAR(50) NOT NULL,
  `authors` TEXT,
  `publish_date` DATETIME, 
  `keywords` TEXT,
  `summary` TEXT, 
  `text` LONGTEXT,
  `url` VARCHAR(200) NOT NULL,
  UNIQUE KEY (`url`),
  `modification_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

