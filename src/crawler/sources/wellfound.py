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
                    # the link's own wrapper only holds the title; walk up until the
                    # container also includes the meta line, stopping before it
                    # grows into the whole job list
                    parent_text = link.evaluate(
                        """el => {
                            let e = el;
                            for (let i = 0; i < 4; i++) {
                                e = e.parentElement;
                                if (!e) break;
                                if (e.querySelectorAll("a[href*='/jobs/']").length > 1) break;
                                if (e.innerText.includes('•')) return e.innerText;
                            }
                            return '';
                        }"""
                    )
                    lines = [l.strip() for l in parent_text.split("\n") if l.strip()]

                    company = None
                    location = None
                    salary = None

                    # parse meta line — "Company • Remote/Onsite • Location • ... • Salary"
                    meta = next((l for l in lines[1:] if "•" in l), None)
                    if meta:
                        parts = [p.strip() for p in meta.split("•")]
                        company = parts[0] or None
                        location = parts[2] if len(parts) > 2 else None
                        salary = next((p for p in parts if "$" in p or "₹" in p), None)
                        if location == salary:
                            location = None

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
