-- Music Library Database Schema
-- MySQL 8.0+

CREATE DATABASE IF NOT EXISTS `music_library`
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `music_library`;

CREATE TABLE IF NOT EXISTS songs (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    title       VARCHAR(255)    NOT NULL,
    artist      VARCHAR(255)    NOT NULL,
    url         TEXT,
    is_favorite TINYINT(1)      NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
