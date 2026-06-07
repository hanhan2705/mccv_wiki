# MVCC Wiki Edit History

Mô phỏng **Multiversion Concurrency Control (MVCC) - Kiểm soát đồng thời đa phiên bản** trên hệ thống wiki phân tán.

> **Ý tưởng cốt lõi:** Thay vì ghi đè, mỗi lần chỉnh sửa tạo ra một **version mới**.
> Readers không bao giờ block Writers, Writers không bao giờ block Readers.

---

## Kiến trúc hệ thống

```
┌─────────────────────────────────────────┐
│              Coordinator                │
│   PageID lẻ → Site A (port 5433)        │
│   PageID chẵn → Site B (port 5434)      │
└────────────┬────────────────┬───────────┘
             │                │
     ┌───────▼──────┐ ┌───────▼──────┐
     │   Site A     │ │   Site B     │
     │  PostgreSQL  │ │  PostgreSQL  │
     │  port 5433   │ │  port 5434   │
     └──────────────┘ └──────────────┘
```

**Dataset schema:**
```sql
Page_Content (PageID, VersionID, Content, Timestamp)
```

---

## Setup

### 1. Khởi động database

```bash
docker-compose up -d
pip install -r requirements.txt
```

### 2. Khởi tạo schema (cả 2 sites)

```bash
# Site A
docker cp sql/schema.sql node_a:/schema.sql
docker exec node_a psql -U admin -d mvcc_wiki -f /schema.sql

# Site B
docker cp sql/schema.sql node_b:/schema.sql
docker exec node_b psql -U admin -d mvcc_wiki -f /schema.sql
```

---

## Chạy demo

Chạy theo thứ tự để thấy đầy đủ các tính năng:

| Bước | Script                         | Mục đích                                                              |
|------|--------------------------------|-----------------------------------------------------------------------|
|  1   | `python _init_db_.py`          | Khởi tạo dữ liệu ban đầu, xem versions đầu tiên được sinh ra          |
|  2   | `python audit_transaction.py`  | Mở giao dịch kiểm toán dài (chờ 10 giây)                              |
|  3   | `python concurrent_writers.py` | Chạy song song ở terminal khác trong lúc giao dịch kiểm toán đang chờ |
|  4   | `python storage_analysis.py`   | Phân tích chi phí lưu trữ khi giữ lại N phiên bản                     |
|  5   | `python failure_demo.py`       | Tắt Site B, chứng minh Site A vẫn hoạt động                           |

> **Tip:** Bước 2 và 3 nên chạy song song trên 2 terminal split để thấy MVCC hoạt động thực tế.

## Failure scenario

```bash
# Tắt Site B
docker stop node_b

# Chạy demo — Site A vẫn phục vụ bình thường
python failure_demo.py

# Khôi phục
docker start node_b
```

---

## Kết quả kỳ vọng

- Audit transaction đọc **consistent snapshot** dù 10 writers đang cập nhật đồng thời
- Site B offline **không làm sập** toàn bộ hệ thống
- Storage overhead **kiểm soát được** bằng giới hạn số version giữ lại (mặc định: 5)
