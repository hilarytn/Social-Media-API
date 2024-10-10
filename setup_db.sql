CREATE DATABASE IF NOT EXISTS social_media_db;
CREATE USER IF NOT EXISTS 'testuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON social_media_db.* TO 'testuser'@'localhost';
FLUSH PRIVILEGES;