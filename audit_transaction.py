from db import get_connection
import time

def run_audit(page_id):
    conn = get_connection()
    conn.autocommit = False
    cursor = conn.cursor()

    # REPEATABLE READ: snapshot được chốt tại thời điểm transaction bắt đầu
    cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")

    print("=== AUDIT STARTED ===")

    # Ghi nhớ VersionID tại thời điểm bắt đầu
    cursor.execute("""
        SELECT VersionID, Content, CreatedAt
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    snapshot_version = cursor.fetchone()
    print(f"[T=0] Snapshot version: {snapshot_version}")

    print("\nSleeping 10 seconds — concurrent writers will run now...\n")
    time.sleep(10)

    # Đọc lại — REPEATABLE READ đảm bảo vẫn thấy snapshot cũ
    cursor.execute("""
        SELECT VersionID, Content, CreatedAt
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    version_after = cursor.fetchone()
    print(f"[T=10s] Version seen inside transaction: {version_after}")

    # Kiểm tra ngoài transaction — version thật sự mới nhất
    conn2 = get_connection()
    cur2 = conn2.cursor()
    cur2.execute("""
        SELECT VersionID, Content, CreatedAt
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    real_latest = cur2.fetchone()
    print(f"[T=10s] REAL latest version in DB: {real_latest}")
    conn2.close()

    # Kết luận
    if snapshot_version[0] == version_after[0]:
        print("\n✅ MVCC confirmed: Audit transaction đọc consistent snapshot!")
    else:
        print("\n⚠️ Snapshot bị thay đổi!")

    conn.commit()
    cursor.close()
    conn.close()
    print("=== AUDIT FINISHED ===")

if __name__ == "__main__":
    run_audit(1)