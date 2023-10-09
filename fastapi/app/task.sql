CREATE TABLE
    `task` (
        `id` int unsigned NOT NULL AUTO_INCREMENT,
        `guest_id` int unsigned NOT NULL,
        `date_time` datetime NOT NULL,
        `name` varchar(256) NOT NULL,
        `details` varchar(512) DEFAULT NULL,
        `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
        `updated_at` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        KEY `guest_id` (`guest_id`),
        CONSTRAINT `task_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
    )