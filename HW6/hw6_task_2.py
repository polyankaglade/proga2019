import logging
import urllib
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List

import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4

logging.basicConfig(
    level=logging.INFO,
    format='%(process)d - %(asctime)s - %(message)s',
)


# logging.info('test')

def get_text(path):
    logging.info('getting text %s', path[-1])
    url = path[-1]
    return path, requests.get(url).text


def links_from_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    content = soup.find("div", {"id": "mw-content-text"})

    links = content.find_all("a")

    for link in links:
        href = link.get('href', '')

        if href.startswith('/wiki'):
            if ':' not in href:

                main_link = 'https://ru.wikipedia.org' + href.split("#")[0]

                yield urllib.parse.unquote(main_link)


def get_links(path, text, end_url):
    # logging.info('getting children %s', path[-1])
    children = []
    links = links_from_text(text)
    for link in links:
        if link == end_url:
            # logging.info('found in %s', url)
            return path, None
        else:
            children.append(link)
    out = [path + [child] for child in set(children)]
    return path, out


def shortest_path(from_article: str, to_article: str, n_threads: int = 10) -> List[str]:
    if from_article == to_article:
        return []

    start_url = 'https://ru.wikipedia.org/wiki/' + from_article
    end_url = 'https://ru.wikipedia.org/wiki/' + to_article

    for url in [start_url, end_url]:
        code = requests.get(url).status_code
        if code == 404:
            raise ValueError(f'{url} does not exist')
        elif 299 < code < 200:
            raise SystemError(f'could not open {url}, got code %d', code)

    executor_text = ProcessPoolExecutor(max_workers=n_threads)
    executor_links = ProcessPoolExecutor(max_workers=n_threads)

    queue = [[start_url]]
    visited = []
    finished = []

    while queue:

        level = []

        future_texts = []
        future_links = []
        for path in queue:
            queue.remove(path)
            node = path[-1]

            if node not in visited:
                visited.append(node)
                # logging.info('executor_text submit %s', node)
                future_text = executor_text.submit(get_text, path)
                future_texts.append(future_text)

        for f_text in as_completed(future_texts):
            path, text = f_text.result()
            # logging.info('executor_link submit %s', path[-1])
            future_link = executor_links.submit(get_links, path, text, end_url)
            future_links.append(future_link)

        for f_links in as_completed(future_links):

            res = f_links.result()

            parent = res[0]
            children = res[1]
            # logging.info('checking %s', parent[-1])

            finished.append(parent[-1])

            if children is None:
                logging.info('finished_len=%s', len(finished))
                full_path = parent[1:] + [end_url]
                final_path = [url.replace('https://ru.wikipedia.org/wiki/', '') for url in full_path]
                logging.info(f'path={final_path}')
                return final_path
            else:
                level.extend(children)
        queue.extend(level)


if __name__ == "__main__":
    logging.info('start')
    print(shortest_path('Теория_струн', 'Динамический_хаос', 10))
    logging.info('end')
