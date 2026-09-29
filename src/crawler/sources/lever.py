import requests
from ..models import Job

SOURCE = "lever"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}

COMPANIES = [
    "meesho",
    "cred",
    "freshworks",
]


def _fetch_company(company: str) -> list[Job]:
    url = f"https://api.lever.co/v0/postings/{company}?mode=json"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    jobs = []
    for item in response.json():
        categories = item.get("categories", {})
        job = Job(
            url=item.get("hostedUrl", ""),
            title=item.get("text", ""),
            company=company.title(),
            location=categories.get("location"),
            source=SOURCE,
            posted_at=None,
        )
        if job.url and job.title:
            jobs.append(job)

    return jobs


def fetch() -> list[Job]:
    jobs = []
    for company in COMPANIES:
        try:
            jobs.extend(_fetch_company(company))
        except Exception:
            continue
    return jobs
