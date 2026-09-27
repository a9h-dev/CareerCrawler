import time
from playwright.sync_api import sync_playwright
from ..models import Job

SOURCE = "naukri"
URL = "https://www.naukri.com/software-engineer-jobs?experience=0"


def fetch() -> list[Job]:
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-IN",
        )
        page = context.new_page()

        try:
            page.goto(URL, wait_until="networkidle", timeout=30000)
            time.sleep(3)

            cards = page.query_selector_all("article.jobTuple, div.srp-jobtuple-wrapper")

            for card in cards[:30]:
                try:
                    title_el = card.query_selector("a.title, a.jobTitle")
                    company_el = card.query_selector("a.subTitle, a.companyName")
                    location_el = card.query_selector("li.location span, span.locWdth")
                    salary_el = card.query_selector("li.salary span, span.salary")

                    title = title_el.inner_text() if title_el else None
                    url = title_el.get_attribute("href") if title_el else None
                    company = company_el.inner_text() if company_el else None
                    location = location_el.inner_text() if location_el else None
                    salary = salary_el.inner_text() if salary_el else None

                    if not title or not url:
                        continue

                    jobs.append(Job(
                        url=url,
                        title=title.strip(),
                        company=company.strip() if company else None,
                        location=location.strip() if location else None,
                        salary=salary.strip() if salary else None,
                        source=SOURCE,
                    ))
                except Exception:
                    continue

        finally:
            browser.close()

    return jobs
