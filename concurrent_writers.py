from wiki_service import edit_page
import threading


def worker(index):
    edit_page(
        1,
        f"Update from Writer {index}"
    )

    print(f"Writer {index} finished")


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

print("\nAll writers finished")