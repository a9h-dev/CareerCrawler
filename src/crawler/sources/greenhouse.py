import requests
from ..models import Job

SOURCE = "greenhouse"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}

COMPANIES = [
    # India
    "groww",
    "slice",
    "appsflyer",
    # Global
    "gitlab",
    "datadog",
    "netlify",
    "planetscale",
    "cloudflare",
    "mongodb",
    "vercel",
    "tailscale",
    "airtable",
]


def _fetch_company(company: str) -> list[Job]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    jobs = []
    for item in response.json().get("jobs", []):
        location = item.get("location", {}).get("name")
        job = Job(
            url=item.get("absolute_url", ""),
            title=item.get("title", ""),
            company=company.title(),
            location=location,
            source=SOURCE,
            posted_at=item.get("updated_at"),
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
