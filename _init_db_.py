import time
from coordinator import get_connection, get_all_connections


def create_page(page_id, content):
    conn = get_connection(page_id)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Page_Content(PageID, Content)
        VALUES (%s, %s)
    """, (page_id, content))
    conn.commit()
    cursor.close()
    conn.close()

    print("Tạo trang thành công!!")


def get_all_versions():
    conns = get_all_connections()

    for site_name, conn in conns.items():
        cur = conn.cursor()
        cur.execute("""
            SELECT pageid, versionid, content
            FROM page_content
            ORDER BY pageid
        """)

        print(f"\nSITE {site_name}")
        for row in cur.fetchall():
            print(f"PageID: {row[0]}, VersionID: {row[1]}, Content: {row[2][:40]}")
        cur.close()
        conn.close()

if __name__ == "__main__":

    print("\n=== Khởi tạo dữ liệu ban đầu cho các Page ===\n")

    pages = [
        (1, "MVCC Introduction"),
        (2, "Database Systems"),
        (3, "Distributed Databases"),
        (4, "Transaction Isolation"),
        (5, "Concurrency Control"),
        (6, "Deadlock Prevention"),
        (7, "Two Phase Commit"),
        (8, "Replication"),
        (9, "Distributed Query Processing"),
        (10, "CAP Theorem")
    ]

    for page_id, content in pages:
        create_page(page_id, content)

    print("\nCurrent Data:")
    get_all_versions()

    print("\n=== Khởi tạo dữ liệu ban đầu hoàn tất. ===\n")