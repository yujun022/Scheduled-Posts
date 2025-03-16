import pymysql
import os
from dotenv import load_dotenv
import time

# 加載 .env 環境變數
load_dotenv()

print("Checking scheduled posts...")

# 取得資料庫連線
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor  # 讓 SQL 結果以字典格式返回
    )

# 發佈定時貼文
def publish_scheduled_posts():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # 找出符合條件的貼文（時間已到，且 is_posted = 0）
        cursor.execute("SELECT id, user_id, content FROM scheduled_posts WHERE posted <= NOW() AND is_posted = 0;")
        posts = cursor.fetchall()

        if posts:
            print(f"Found {len(posts)} posts to publish.")

        for post in posts:
            post_id, user_id, content = post["id"], post["user_id"], post["content"]

            # 插入到 posts 表
            cursor.execute("INSERT INTO posts (user_id, content) VALUES (%s, %s);", (user_id, content))

            # 更新 is_posted = 1
            cursor.execute("UPDATE scheduled_posts SET is_posted = 1 WHERE id = %s;", (post_id,))
            db.commit()

            print(f"Published post ID {post_id}.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()

# 讓程式一直運行，每 60 秒執行一次
while True:
    publish_scheduled_posts()
    print("Waiting for next check...")
    time.sleep(60)  # 60 秒後再檢查一次
