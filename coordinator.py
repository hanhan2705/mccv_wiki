import psycopg2

SITES = {
    "A": {"host": "localhost", "port": 5433, "description": "PageID lẻ (1, 3, 5...)"},
    "B": {"host": "localhost", "port": 5434, "description": "PageID chẵn (2, 4, 6...)"},
}

DATABASE = "mvcc_wiki"
USER     = "admin"
PASSWORD = "admin"


def get_site_name(page_id: int) -> str:
    return "A" if page_id % 2 == 1 else "B"


def get_connection(page_id: int):
    site_name = get_site_name(page_id)
    site = SITES[site_name]
    return psycopg2.connect(
        host=site["host"],
        port=site["port"],
        database=DATABASE,
        user=USER,
        password=PASSWORD,
    )


def get_all_connections() -> dict:
    """Trả về connection tới tất cả sites — dùng cho cross-site query."""
    conns = {}
    for name, site in SITES.items():
        try:
            conns[name] = psycopg2.connect(
                host=site["host"],
                port=site["port"],
                database=DATABASE,
                user=USER,
                password=PASSWORD,
            )
        except Exception as e:
            print(f"[Coordinator] Site {name} ({site['port']}) offline: {e}")
            conns[name] = None
    return conns


if __name__ == "__main__":
    print("=== Coordinator routing table ===")
    for name, site in SITES.items():
        print(f"  Site {name} — port {site['port']} — {site['description']}")

    print("\n=== Kiểm tra kết nối ===")
    for test_page in [1, 2, 3, 4]:
        site = get_site_name(test_page)
        print(f"  PageID {test_page} → Site {site}")