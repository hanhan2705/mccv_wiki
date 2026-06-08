from coordinator import get_all_connections

def clear():
    conns = get_all_connections()
    for site_name, conn in conns.items():
        if conn is None:
            print(f"Site {site_name} offline")
            continue

        cursor = conn.cursor()
        cursor.execute("""
            TRUNCATE TABLE Page_Content RESTART IDENTITY
        """)
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Đã xóa dữ liệu Site {site_name}")

if __name__ == "__main__":
    clear()
    print("Đã xóa sạch dữ liệu trong tất cả sites!")