import time
from playwright.sync_api import sync_playwright
from ..models import Job

SOURCE = "indeed"
SEARCH_URL = "https://www.indeed.com/jobs?q=software+engineer&l=remote&sort=date"


def fetch() -> list[Job]:
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
        )
        page = context.new_page()

        try:
            page.goto(SEARCH_URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(3)  # let JS render

            cards = page.query_selector_all("div.job_seen_beacon")

            for card in cards[:30]:
                try:
                    title_el = card.query_selector("h2.jobTitle span[title]")
                    company_el = card.query_selector("[data-testid='company-name']")
                    location_el = card.query_selector("[data-testid='text-location']")
                    salary_el = card.query_selector("[data-testid='attribute_snippet_testid']")
                    link_el = card.query_selector("h2.jobTitle a")

                    title = title_el.get_attribute("title") if title_el else None
                    company = company_el.inner_text() if company_el else None
                    location = location_el.inner_text() if location_el else None
                    salary = salary_el.inner_text() if salary_el else None
                    href = link_el.get_attribute("href") if link_el else None

                    if not title or not href:
                        continue

                    url = f"https://www.indeed.com{href}" if href.startswith("/") else href

                    jobs.append(Job(
                        url=url,
                        title=title,
                        company=company,
                        location=location,
                        salary=salary,
                        source=SOURCE,
                    ))
                except Exception:
                    continue

        finally:
            browser.close()

    return jobs
