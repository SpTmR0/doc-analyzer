from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

def fetch_article_text(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=100)  #headless is false(direct chrome opener) as it was not working for true/indirect
            page = browser.new_page()
            page.goto(url, timeout=60000)
            time.sleep(8)                                             #giving Cloudflare 5–8 seconds to finish bot check
            html = page.content()
            browser.close()

        soup = BeautifulSoup(html, "html.parser")

        article = (soup.find("div", class_="article__body"))

        if not article:
            return "Article content not found. HTML structure may have changed."

        raw_text = article.get_text(separator="\n").strip()
        cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])

        return cleaned_text, html
    
    except Exception as e:
        raise RuntimeError(f"Playwright error: {str(e)}")
