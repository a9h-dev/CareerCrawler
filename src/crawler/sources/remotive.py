import requests
from ..models import Job

SOURCE = "remotive"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}
URL = "https://remotive.com/api/remote-jobs"


def fetch() -> list[Job]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    jobs = []
    for item in response.json().get("jobs", []):
        job = Job(
            url=item.get("url", ""),
            title=item.get("title", ""),
            company=item.get("company_name"),
            location=item.get("candidate_required_location"),
            salary=item.get("salary"),
            source=SOURCE,
            posted_at=item.get("publication_date"),
        )
        if job.url and job.title:
            jobs.append(job)

    return jobs
