CREATE DATABASE IF NOT EXISTS rasset;

USE rasset;

CREATE TABLE IF NOT EXISTS mrm_chiefs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tgid INT NOT NULL,
    tgusername VARCHAR(255),
    tgfullname VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tgid INT NOT NULL,
    birthday DATE,
    tgusername VARCHAR(255),
    location VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tgid INT NOT NULL,
    tgusername VARCHAR(255)
);
