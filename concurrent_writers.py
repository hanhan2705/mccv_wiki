from wiki_service import edit_page
import threading

print("\n=== 10 Writer đồng thời cập nhật PageID=1 ===\n")
def worker(index):
    edit_page(
        1,
        f"Update from Writer {index}."
    )

    print(f"Writer {index} hoàn thành cập nhật.")


threads = []

for i in range(10):
    t = threading.Thread(
        target=worker,
        args=(i + 1,)
    )

    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n Tất cả các writer đều cập nhật hoàn tất.\n")