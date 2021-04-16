import concurrent.futures
import time

from cfg import SLEEPTIME
from common import rishennya, get_list_rishen, load_visited_links, store_link, send_to_check

if __name__ == '__main__':
    print("Program has been started")
    while True:
        try:
            rishennya_urls = get_list_rishen()
            poseshennyi = load_visited_links()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for url in rishennya_urls[:3]:
                    if url not in poseshennyi:
                        futures.append(executor.submit(rishennya, url=url))
                docs = []
                for future in concurrent.futures.as_completed(futures):
                    doc = future.result()
                    docs.append(doc)
                    print(docs)
                futures = []
                for i in docs:
                    futures.append(executor.submit(send_to_check, i))
                    store_link(i)
                for future in concurrent.futures.as_completed(futures):
                    doc_ = future.result()
        except Exception as e:
            print("Exception occurred")
        print("Program has been ended, next start will be in 1 hour")
        time.sleep(SLEEPTIME)