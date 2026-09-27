import requests
from ..models import Job

SOURCE = "jobicy"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}
URL = "https://jobicy.com/api/v2/remote-jobs?count=50&industry=engineering"


def fetch() -> list[Job]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    jobs = []
    for item in response.json().get("jobs", []):
        job = Job(
            url=item.get("url", ""),
            title=item.get("jobTitle", ""),
            company=item.get("companyName"),
            location=item.get("jobGeo"),
            salary=item.get("annualSalaryMin") and f"${item['annualSalaryMin']}–${item['annualSalaryMax']}",
            source=SOURCE,
            posted_at=item.get("pubDate"),
        )
        if job.url and job.title:
            jobs.append(job)

    return jobs
