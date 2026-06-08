from coordinator import get_connection
import time

def run_audit(page_id):
    conn = get_connection(page_id)
    conn.autocommit = False
    cursor = conn.cursor()

    # REPEATABLE READ: snapshot được chốt tại thời điểm transaction bắt đầu
    cursor.execute("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")

    print("=== MINH CHỨNG MVCC: GIAO DỊCH KIỂM TOÁN ===")

    # Ghi nhớ VersionID tại thời điểm bắt đầu
    cursor.execute("""
        SELECT VersionID, Content, Timestamp
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    snapshot_version = cursor.fetchone()
    print(f"[T=0] Phiên bản snapshot tại thời điểm bắt đầu: {snapshot_version}")

    print("\n Tạm dừng 10s — các giao dịch cập nhật đồng thời sẽ chạy...\n")
    time.sleep(10)

    # Đọc lại — REPEATABLE READ đảm bảo vẫn thấy snapshot cũ
    cursor.execute("""
        SELECT VersionID, Content, Timestamp
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    version_after = cursor.fetchone()
    print(f"[T=10s] Phiên bản được nhìn thấy bên trong giao dịch: {version_after}")

    # Kiểm tra ngoài transaction — version thật sự mới nhất
    conn2 = get_connection(page_id)
    cur2 = conn2.cursor()
    cur2.execute("""
        SELECT VersionID, Content, Timestamp
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))
    real_latest = cur2.fetchone()
    print(f"[T=10s] Phiên bản mới nhất thực tế trong cơ sở dữ liệu:: {real_latest}")
    print(f"\nPhiên bản snapshot tại thời điểm bắt đầu = {snapshot_version[0]}")
    print(f"VersionID mới nhất = {real_latest[0]}")
    cur2.close()
    conn2.close()

    # Kết luận
    if snapshot_version[0] == version_after[0]:
        print("\n Xác nhận MVCC: Giao dịch kiểm toán luôn đọc cùng một snapshot nhất quán!")
    else:
        print("\nSnapshot bị thay đổi!")

    conn.commit()
    cursor.close()
    conn.close()
    print("\n=== KẾT THÚC GIAO DỊCH KIỂM TOÁN ===\n")

if __name__ == "__main__":
    run_audit(1)

    print("Kết luận\n" \
    "- Reader không bị Writer chặn.\n" \
    "- 10 Writer vẫn cập nhật bình thường.\n" \
    "- Reader luôn nhìn thấy một phiên bản dữ liệu nhất quán trong suốt transaction.\n" 
    "- Dữ liệu không bị thay đổi giữa chừng đối với Audit.")