from wiki_service import (
    edit_page,
    get_latest_version
)

edit_page(
    1,
    "Version created from MVCC service"
)

latest = get_latest_version(1)

print("\nLatest Version:")
print(latest)