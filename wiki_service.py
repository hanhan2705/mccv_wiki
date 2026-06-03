from db import get_connection


def edit_page(page_id, new_content, max_versions=5):
    conn = get_connection()
    try:
        cursor = conn.cursor()

        # INSERT version mới
        cursor.execute("""
            INSERT INTO Page_Content(PageID, Content)
            VALUES (%s, %s)
        """, (page_id, new_content))

        # Xóa version cũ, chỉ giữ lại max_versions gần nhất
        cursor.execute("""
            DELETE FROM Page_Content
            WHERE PageID = %s
              AND VersionID NOT IN (
                SELECT VersionID
                FROM Page_Content
                WHERE PageID = %s
                ORDER BY VersionID DESC
                LIMIT %s
              )
        """, (page_id, page_id, max_versions))

        conn.commit()
        print(f"New version created! (kept last {max_versions} versions)")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

def get_latest_version(page_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 1
    """, (page_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result

