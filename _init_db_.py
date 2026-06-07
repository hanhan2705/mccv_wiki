import time
from db import get_connection

def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

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

    slow_print("\n=== Khởi tạo dữ liệu ban đầu cho các Page ===\n", 0.02)

    pages = [
        (1, "MVCC Introduction"),
        (2, "Database Systems"),
        (3, "Distributed Databases"),
        (4, "Transaction Isolation"),
        (5, "Concurrency Control")
    ]

    for page_id, content in pages:
        create_page(page_id, content)

    slow_print("\nCurrent Data:", 0.02)
    for row in get_all_versions():
        slow_print(f"PageID: {row[0]}, VersionID: {row[1]}, Content: {row[2][:40]}", 0.01)

    slow_print("\n=== Khởi tạo dữ liệu ban đầu hoàn tất. ===\n", 0.02)