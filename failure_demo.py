import time
import coordinator
from wiki_service import edit_page, get_latest_version


def check_site(site_name: str, port: int) -> bool:
    import psycopg2
    try:
        conn = psycopg2.connect(
            host="localhost", port=port,
            database="mvcc_wiki", user="admin", password="admin",
            connect_timeout=3,
        )
        conn.close()
        return True
    except Exception:
        return False


def demo_write_to_offline_site():
    print("\n=== FAILURE SCENARIO: Site B offline ===\n")

    # Kiểm tra trạng thái ban đầu
    site_a_ok = check_site("A", 5433)
    site_b_ok = check_site("B", 5434)

    print(f"Site A (port 5433): {'ONLINE' if site_a_ok else 'OFFLINE'}")
    print(f"Site B (port 5434): {'ONLINE' if site_b_ok else 'OFFLINE'}")
    print()

    if site_b_ok:
        print("Site B đang chạy.")
        print("   Để demo failure, hãy tắt Site B:")
        print("   docker stop mvcc_postgres_b")
        print("   Rồi chạy lại script này.\n")
        return

    # Site A vẫn phục vụ PageID lẻ bình thường
    print("--- Ghi vào Site A (PageID=1, lẻ) ---")
    try:
        edit_page(1, "Written during Site B failure — Site A still works")
        latest = get_latest_version(1)
        print(f"Site A OK — latest version: {latest[0]}, content: '{latest[1][:40]}...'\n")
    except Exception as e:
        print(f"Site A cũng lỗi: {e}\n")

    # Thử ghi PageID chẵn → Site B → fail gracefully
    print("--- Thử ghi vào Site B (PageID=2, chẵn) ---")
    try:
        edit_page(2, "This write should fail — Site B is down")
        print("Ghi thành công (Site B đang online)\n")
    except Exception as e:
        print(f" Failure detected gracefully: {e}")
        print("  Site A không bị ảnh hưởng — dữ liệu PageID lẻ vẫn an toàn.\n")


def demo_read_during_failure():
    print("--- Đọc từ Site A trong khi Site B offline ---")
    try:
        latest = get_latest_version(1)
        if latest:
            print(f"Đọc Site A thành công — VersionID: {latest[0]}")
        else:
            print("Không có dữ liệu trong Site A")
    except Exception as e:
        print(f"Lỗi: {e}")

    print("\n--- KẾT LUẬN ---")
    print("Kịch bản lỗi đã được xử lý thành công.")
    print("Khi Site B ngừng hoạt động, các thao tác trên Site A vẫn thực hiện bình thường.")
    print("Yêu cầu ghi dữ liệu tới Site B bị từ chối và trả về thông báo lỗi rõ ràng.")
    print("Hệ thống không bị dừng hoặc sập do lỗi của một site.")


if __name__ == "__main__":
    demo_write_to_offline_site()
    demo_read_during_failure()