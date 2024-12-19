from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def fetch_url(url):
    """Загружает содержимое страницы по URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка при загрузке {url}: статус {response.status}")
                return None


def extract_links(html):
    """Извлекает внешние ссылки из HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        if link.startswith('http') and not link.startswith('mailto:'):
            links.add(link)
    return links


async def crawl(start_urls, max_iterations=3):
    """Запускает краулер по заданным ссылкам ."""
    visited = set()
    to_visit = set(start_urls)

    for _ in range(max_iterations):
        if not to_visit:
            break

        current_to_visit = list(to_visit)
        to_visit.clear()

        for url in current_to_visit:
            if url in visited:
                continue

            print(f"Посещение: {url}")
            visited.add(url)
            html = await fetch_url(url)

            if html:
                links = extract_links(html)
                to_visit.update(links - visited)

    with open('found_links.txt', 'w') as f:
        for link in visited:
            f.write(f"{link}\n")


if __name__ == '__main__':
    start_urls = ["https://en.wikipedia.org/wiki/Main_Page", "https://www.google.com","https://yandex.ru/pogoda"]
    asyncio.run(crawl(start_urls, max_iterations=3))
