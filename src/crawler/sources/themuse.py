import requests
from ..models import Job

SOURCE = "themuse"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}
URL = "https://www.themuse.com/api/public/jobs?category=Software%20Engineer&page=0"


def fetch() -> list[Job]:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status()

    jobs = []
    for item in response.json().get("results", []):
        locations = item.get("locations", [])
        location = locations[0].get("name") if locations else None

        job = Job(
            url=item.get("refs", {}).get("landing_page", ""),
            title=item.get("name", ""),
            company=item.get("company", {}).get("name"),
            location=location,
            source=SOURCE,
            posted_at=item.get("publication_date"),
        )
        if job.url and job.title:
            jobs.append(job)

    return jobs
