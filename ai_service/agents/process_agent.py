import httpx
from bs4 import BeautifulSoup

async def fetch_content(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")

            paragraphs = [p.get_text() for p in soup.find_all("p")]
            return " ".join(paragraphs[:20])
    except:
        return ""

async def process(results):
    processed = []

    for item in results:
        content = await fetch_content(item["url"])

        processed.append({
            "title": item["title"],
            "url": item["url"],
            "content": content
        })

    return processed