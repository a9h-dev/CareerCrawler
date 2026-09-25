import requests
from ..models import Job

SOURCE = "hackernews"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}

SEARCH_URL = "https://hn.algolia.com/api/v1/search?query=Ask+HN%3A+Who+is+hiring&tags=ask_hn&hitsPerPage=1"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def _get_latest_hiring_post_id() -> int:
    response = requests.get(SEARCH_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()["hits"][0]["objectID"]


def _get_comments(post_id: int) -> list[int]:
    response = requests.get(ITEM_URL.format(post_id), headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json().get("kids", [])


def _parse_comment(comment_id: int) -> Job | None:
    response = requests.get(ITEM_URL.format(comment_id), headers=HEADERS, timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("dead") or data.get("deleted"):
        return None

    text = data.get("text", "")
    url = f"https://news.ycombinator.com/item?id={comment_id}"

    first_line = text.split("<p>")[0].strip()
    parts = [p.strip() for p in first_line.split("|")]

    company = parts[0] if len(parts) > 0 else None
    title = parts[1] if len(parts) > 1 else first_line
    location = parts[2] if len(parts) > 2 else None

    return Job(
        url=url,
        title=title,
        company=company,
        location=location,
        source=SOURCE,
    )


def fetch() -> list[Job]:
    post_id = _get_latest_hiring_post_id()
    comment_ids = _get_comments(post_id)

    jobs = []
    for comment_id in comment_ids[:50]:
        job = _parse_comment(comment_id)
        if job and job.title:
            jobs.append(job)

    return jobs
