# MVCC Wiki Edit History

Mô phỏng Multiversion Concurrency Control (MVCC) trên hệ thống wiki.

## Setup

```bash
docker-compose up -d
pip install -r requirements.txt
```

## Khởi tạo database

```bash
psql -h localhost -p 5433 -U admin -d mvcc_wiki -f sql/schema.sql
# Chạy schema
docker cp sql/schema.sql mvcc_postgres:/schema.sql
docker exec mvcc_postgres psql -U admin -d mvcc_wiki -f /schema.sql 
```

## Chạy demo

| Script | Mục đích |
|---|---|
| `python test_insert.py` | Tạo page đầu tiên |
| `python concurrent_writers.py` | 10 writers đồng thời |
| `python audit_transaction.py` | Audit transaction đọc consistent snapshot |
| `python storage_analysis.py` | Phân tích storage overhead |