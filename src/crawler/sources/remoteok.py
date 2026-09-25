import requests
from ..models import Job

URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}
SOURCE = "remoteok"


def fetch() -> list[Job]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    data = response.json()
    data = data[1:]  # first item is metadata, skip it

    jobs = []
    for item in data:
        job = Job(
            url=item.get("url", ""),
            title=item.get("position", ""),
            company=item.get("company"),
            location=item.get("location"),
            salary=item.get("salary"),
            source=SOURCE,
            posted_at=item.get("date"),
        )
        if job.url and job.title:  # skip incomplete listings
            jobs.append(job)

    return jobs
