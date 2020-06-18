CREATE TABLE `fb_group_posts_reactions` (
 `Reaction ID` varchar(400) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Facebook Post ID` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
 `Scraped DateTime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
 `Posted By` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
 PRIMARY KEY (`Reaction ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci