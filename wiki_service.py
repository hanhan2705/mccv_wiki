import coordinator

def edit_page(page_id: int, new_content: str, max_versions: int = 5):
    conn = coordinator.get_connection(page_id)
    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Page_Content(PageID, Content)
            VALUES (%s, %s)
        """, (page_id, new_content))

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
        site = coordinator.get_site_name(page_id)
        print(f"[Site {site}] New version created for PageID={page_id} (kept last {max_versions})")

    except Exception as e:
        conn.rollback()
        print(f"[wiki_service] Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_latest_version(page_id: int):
    conn = coordinator.get_connection(page_id)
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


def get_version_history(page_id: int, limit: int = 5):
    conn = coordinator.get_connection(page_id)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT VersionID, Content, CreatedAt
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT %s
    """, (page_id, limit))

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows