CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    userid VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);


CREATE TABLE youtube_categories (
    category_id INT PRIMARY KEY,       -- 유튜브 API에서 받은 카테고리 ID (직접 지정)
    category_name VARCHAR(255) NOT NULL UNIQUE  -- 카테고리 이름
);


CREATE TABLE youtube_keywords (
    keyword_id INT PRIMARY KEY AUTO_INCREMENT,  -- 키워드 ID (자동 증가)
    keyword VARCHAR(255) NOT NULL,               -- 키워드
    category_id INT NOT NULL,                    -- 유튜브 API 카테고리 ID
    median_likes INT DEFAULT 0,                  -- 좋아요 중간값
    median_comments INT DEFAULT 0,               -- 댓글 수 중간값
    avg_views INT DEFAULT 0,                     -- 평균 조회수
    mention_count INT DEFAULT 0,                 -- 언급량
    FOREIGN KEY (category_id) REFERENCES youtube_categories(category_id) 
        ON DELETE CASCADE  -- 카테고리 삭제 시 키워드도 삭제
);

INSERT INTO youtube_categories (category_id, category_name) VALUES 
(1, 'Film & Animation'),
(10, 'Music'),
(15, 'Pets & Animals'),
(17, 'Sports'),
(20, 'Gaming'),
(24, 'Entertainment'),
(25, 'News & Politics'),
(28, 'Science & Technology');
