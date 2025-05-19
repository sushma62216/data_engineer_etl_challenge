CREATE TABLE IF NOT EXISTS staging_users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    username VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS staging_posts (
    id INT PRIMARY KEY,
    userId INT,
    title TEXT,
    body TEXT
);
