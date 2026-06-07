from db import get_connection

def create_page(page_id, content):
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Page_Content
        ORDER BY PageID, VersionID
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

if __name__ == "__main__":

    pages = [
        (1, "MVCC Introduction"),
        (2, "Database Systems"),
        (3, "Distributed Databases"),
        (4, "Transaction Isolation"),
        (5, "Concurrency Control")
    ]

    for page_id, content in pages:
        create_page(page_id, content)

    print("\nCurrent Data:")

    for row in get_all_versions():
        print(row)

    print("\n=== Khởi tạo dữ liệu ban đầu hoàn tất. ===\n")