from cfg import SLEEPTIME
from pydantic import BaseModel
import concurrent.futures
import time
from common import rishennya, parse, load_visited_links, store_link, send_to_check


class Document(BaseModel):
    title: str
    link: str
    file_content: str
    file_name: str


if __name__ == '__main__':
    print("nachinaem")
    while True:
        try:
            rishennya_urls = parse()
            poseshennyi = load_visited_links()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for url in rishennya_urls[:2]:
                    if url not in poseshennyi:
                        futures.append(executor.submit(rishennya, url=url))
                docs = []

                for future in concurrent.futures.as_completed(futures):
                    doc = future.result()
                    docs.append(doc)
                    print(doc.title)
                futures = []
                for i in docs:
                    futures.append(executor.submit(send_to_check, i))
                    store_link(i)
                for future in concurrent.futures.as_completed(futures):
                    doc_ = future.result()
        except Exception as e:
            print("Exception occurred")
        print("nachinaem spat")
        time.sleep(SLEEPTIME)