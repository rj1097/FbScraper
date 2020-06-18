CREATE TABLE `fb_group_post_comments` (
 `Comment ID` varchar(600) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Comment Post ID` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Comment Posted DateTime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 `Reply` enum('Yes','No') COLLATE utf8mb4_unicode_ci NOT NULL,
 `Parent Comment ID` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
 `Posted By` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Comment Content` blob NOT NULL,
 PRIMARY KEY (`Comment ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci