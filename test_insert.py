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

    print("Page created successfully!")


def get_all_versions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Page_Content
        ORDER BY VersionID
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


if __name__ == "__main__":
    create_page(
        1,
        "MVCC Introduction from Python"
    )

    print("\nCurrent Data:")

    for row in get_all_versions():
        print(row)