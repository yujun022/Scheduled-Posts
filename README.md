# Scheduled-Posts

# 設定說明

## 1. 環境需求

-	Python 3.8+
-	MySQL 資料庫
  
## 2 . 安裝依賴套件
```bash
pip install -r requirements.txt
```
## 3. 設定環境變數
請在專案根目錄建立 .env 檔案，可參考已提供的 .env.example 檔案，內容格式如下:
```bash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=plurk
```
## 4. 建立資料庫

```
source schema.sql;
source post.sql;
```

## 5. 運行專案
啟動 FastAPI 伺服器
```
uvicorn main:app --reload
```

啟動排程系統
```
python scheduler.py
```

# API 文件
## 1. 獲取所有預約貼文
### GET /api/scheduled_posts
```
[
  {
    "id": 1,
    "content": "這是一則預約貼文",
    "posted": "2025-03-15T22:45:00",
    "is_posted": false,
    "user_id": 1
  },
  ...
]
```
## 2. 新增預約貼文
### POST /api/scheduled_posts
```
{
  "content": "這是一則新的預約貼文",
  "posted": "2025-03-15T23:00:00",
  "user_id": 1
}
```
## 3. 編輯預約貼文
### PUT /api/scheduled_posts/{id}
```
{
  "content": "修改後的內容",
  "posted": "2025-03-16T10:00:00"
}
```
## 4. 刪除預約貼文
### DELETE /api/scheduled_posts/{id}
```
{
  "content": "修改後的內容",
  "posted": "2025-03-16T10:00:00"
}
```

# 測試說明
## 測試排程功能
### 執行以下指令，每隔 60 秒會檢查是否有需要發佈的貼文
```
python scheduler.py
```

# 設計決策與假設
-	預約貼文存放於 scheduled_posts 資料表，欄位包括 id、content、posted、is_posted、user_id、created_at
-	當時間達到 posted 時，scheduler.py 將自動檢查並將貼文移至 posts 資料表，同時更新 is_posted 為 TRUE
-	預約噗文在發佈時間到達時，會由 scheduler.py 插入到 posts 資料表，意味著其他用戶在瀏覽時間軸時，會自動看到該預約噗文，無需額外操作

