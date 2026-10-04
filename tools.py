from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web and return multiple relevant sources with titles, URLs and snippets."""

    results = tavily.search(
        query=query,
        max_results=5
    )

    out = []

    for i, r in enumerate(results["results"], 1):
        out.append(
            f"Source {i}\n"
            f"Title: {r['title']}\n"
            f"URL: {r['url']}\n"
            f"Snippet: {r['content'][:500]}\n"
        )

    return "\n----\n".join(out)


@tool
def scrape_urls(urls: str) -> str:
    """Scrape multiple URLs and return cleaned content from each source."""

    url_list = [url.strip() for url in urls.split("\n") if url.strip()]

    all_content = []

    for i, url in enumerate(url_list[:5], 1):
        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside"
            ]):
                tag.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            text = " ".join(text.split())

            all_content.append(
                f"===== SOURCE {i} =====\n"
                f"URL: {url}\n"
                f"CONTENT:\n{text[:4000]}\n"
            )

        except Exception as e:
            all_content.append(
                f"===== SOURCE {i} =====\n"
                f"URL: {url}\n"
                f"ERROR: Could not scrape this source: {str(e)}\n"
            )

    return "\n".join(all_content)


# Backward compatibility
@tool
def scrape_url(url: str) -> str:
    """Scrape a single URL."""

    return scrape_urls.invoke(url)