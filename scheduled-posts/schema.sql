CREATE TABLE scheduled_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    posted DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_posted BOOLEAN DEFAULT FALSE
);

INSERT INTO scheduled_posts (user_id, content, posted) 
VALUES (1, 'This is a scheduled post.', NOW() + INTERVAL 1 MINUTE);
