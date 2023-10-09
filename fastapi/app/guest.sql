CREATE TABLE
    `guest` (
        `id` int unsigned NOT NULL AUTO_INCREMENT,
        `full_name` varchar(256) NOT NULL,
        `alt_name` varchar(256) DEFAULT NULL,
        `salute` varchar(10) DEFAULT NULL,
        `title` varchar(128) DEFAULT NULL,
        `organization` varchar(256) DEFAULT NULL,
        `country` varchar(128) DEFAULT NULL,
        `email` varchar(256) DEFAULT NULL,
        `phone` varchar(256) DEFAULT NULL,
        `details` varchar(1024) DEFAULT NULL COMMENT 'Details in JSON String',
        `hash` varchar(10) DEFAULT NULL COMMENT '',
        `is_deleted` tinyint(1) DEFAULT '0',
        `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        UNIQUE KEY `hash` (`hash`)
    )