import time

from db import get_connection


def count_versions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM Page_Content
    """)

    total_versions = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total_versions


def table_size():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT pg_size_pretty(
            pg_total_relation_size('page_content')
        );
    """)

    size = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return size


def historical_read_test(page_id):
    conn = get_connection()
    cursor = conn.cursor()

    start_time = time.perf_counter()

    cursor.execute("""
        SELECT *
        FROM Page_Content
        WHERE PageID = %s
        ORDER BY VersionID DESC
        LIMIT 5
    """, (page_id,))

    rows = cursor.fetchall()

    end_time = time.perf_counter()

    elapsed_ms = (end_time - start_time) * 1000

    cursor.close()
    conn.close()

    return elapsed_ms, rows


def versions_per_page():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            PageID,
            COUNT(*) AS VersionCount
        FROM Page_Content
        GROUP BY PageID
        ORDER BY PageID
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def compare_storage_overhead(page_id, max_versions_list=[1, 3, 5, 10, None]):
    """
    Mô phỏng: nếu chỉ giữ N version thì table size thay đổi thế nào?
    """
    print("\n===== VERSION LIMIT COMPARISON =====")
    print(f"{'Max Versions':<15} {'Rows Kept':<12} {'Est. Size'}")
    print("-" * 45)

    conn = get_connection()
    cursor = conn.cursor()

    # Lấy tổng số version của page
    cursor.execute("""
        SELECT COUNT(*), pg_size_pretty(pg_total_relation_size('page_content'))
        FROM Page_Content WHERE PageID = %s
    """, (page_id,))
    total, full_size = cursor.fetchone()

    for limit in max_versions_list:
        label = str(limit) if limit else "All"
        kept = min(total, limit) if limit else total
        # Ước tính dung lượng theo tỉ lệ
        ratio = kept / total if total > 0 else 0
        print(f"{label:<15} {kept:<12} ~{ratio*100:.0f}% of {full_size}")

    cursor.close()
    conn.close()


if __name__ == "__main__":

    print("\n===== STORAGE ANALYSIS =====\n")

    total_versions = count_versions()
    print(f"Total Versions Stored: {total_versions}")

    size = table_size()
    print(f"Table Size: {size}")

    print("\nVersions Per Page:")
    for page in versions_per_page():
        print(
            f"Page {page[0]} -> {page[1]} versions"
        )

    elapsed_ms, rows = historical_read_test(1)

    print("\nHistorical Read Test")
    print(f"Execution Time: {elapsed_ms:.4f} ms")
    print(f"Rows Returned: {len(rows)}")

    print("\nLatest Historical Records:")

    for row in rows:
        print(row)

    print("\n===== END ANALYSIS =====")