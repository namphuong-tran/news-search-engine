-- USE `temp_db`;
-- DROP TABLE IF EXISTS `temp_table`;
-- CREATE TABLE `temp_table` (
--   `id` INT NOT NULL AUTO_INCREMENT,
--   PRIMARY KEY (`id`),
--   `field` VARCHAR(255) NOT NULL,
--   `update_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
-- );
-- INSERT INTO temp_table (id, field) VALUES (1, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (2, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (3, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (4, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (5, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (6, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (7, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (8, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (9, 'dummy field');
-- INSERT INTO temp_table (id, field) VALUES (10, 'dummy field');







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

