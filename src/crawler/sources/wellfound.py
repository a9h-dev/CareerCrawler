import time
from playwright.sync_api import sync_playwright
from ..models import Job

SOURCE = "wellfound"
URL = "https://wellfound.com/jobs?role=software-engineer"
BASE = "https://wellfound.com"


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
            page.goto(URL, wait_until="domcontentloaded", timeout=30000)
            time.sleep(6)

            links = page.query_selector_all("a[href*='/jobs/']")

            for link in links:
                try:
                    href = link.get_attribute("href")
                    title = link.inner_text().strip()

                    if not href or not title or "signup" in href or len(title) < 3:
                        continue

                    # get the parent container text for company/location/salary
                    parent_text = link.evaluate("el => el.closest('div') ? el.closest('div').innerText : ''")
                    lines = [l.strip() for l in parent_text.split("\n") if l.strip()]

                    company = lines[1] if len(lines) > 1 else None
                    location = None
                    salary = None

                    # parse meta line — usually "Company • Location • Salary"
                    if len(lines) > 1:
                        meta = lines[1]
                        parts = [p.strip() for p in meta.split("•")]
                        if len(parts) >= 2:
                            company = parts[0]
                            location = parts[1] if len(parts) > 1 else None
                            salary = next((p for p in parts if "$" in p), None)

                    url = BASE + href if href.startswith("/") else href

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
