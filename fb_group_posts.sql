CREATE TABLE `fb_group_posts` (
 `Facebook Post ID` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Facebook Post Content` blob NOT NULL,
 `Post DateTime` timestamp NOT NULL DEFAULT current_timestamp(),
 `Posted By` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Live Session Video` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Group ID` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
 PRIMARY KEY (`Facebook Post ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci