from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from datetime import datetime
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()  # 加載 .env 文件中的環境變數

# 連接到 MySQL 資料庫
db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor  # 確保返回字典格式
)
cursor = db.cursor()

app = FastAPI()

# 定義預約噗文的 Pydantic 模型
class ScheduledPost(BaseModel):
    content: str
    posted: datetime
    user_id: int

# 新增噗文功能
@app.post("/api/scheduled_posts")
async def create_scheduled_post(post: ScheduledPost):
    try:
        cursor.execute("""
            INSERT INTO scheduled_posts (user_id, content, posted)
            VALUES (%s, %s, %s);
        """, (post.user_id, post.content, post.posted))
        db.commit()
        return {"message": "Scheduled post created successfully", "data": post}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error saving to database: {e}")

# 瀏覽噗文功能
@app.get("/api/scheduled_posts")
async def get_scheduled_posts():
    cursor.execute("SELECT * FROM scheduled_posts")
    posts = cursor.fetchall()
    return {"scheduled_posts": posts}

# 刪除噗文功能
@app.delete("/api/scheduled_posts/{post_id}")
async def delete_scheduled_post(post_id: int):
    cursor.execute("SELECT * FROM scheduled_posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        cursor.execute("DELETE FROM scheduled_posts WHERE id = %s", (post_id,))
        db.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting post: {e}")

class UpdateScheduledPost(BaseModel):
    content: str | None = None
    posted: datetime | None = None

# 編輯噗文功能
@app.put("/api/scheduled_posts/{post_id}")
async def update_scheduled_post(post_id: int, post: UpdateScheduledPost):
    cursor.execute("SELECT * FROM scheduled_posts WHERE id = %s", (post_id,))
    existing_post = cursor.fetchone()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    try:
        if post.content is not None:
            cursor.execute("UPDATE scheduled_posts SET content = %s WHERE id = %s", (post.content, post_id))
        if post.posted is not None:
            cursor.execute("UPDATE scheduled_posts SET posted = %s WHERE id = %s", (post.posted, post_id))
        db.commit()
        return {"message": "Post updated successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating post: {e}")
