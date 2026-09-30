import requests
from ..models import Job

SOURCE = "lever"
HEADERS = {"User-Agent": "CareerCrawler/1.0"}

COMPANIES = [
    # India
    "meesho",
    "cred",
    "freshworks",
    "paytm",
    "razorpay",
    "zerodha",
    "phonepe",
    "swiggy",
    "zomato",
    "ola",
    "unacademy",
    "lenskart",
    "nykaa",
    "cars24",
    "delhivery",
    "darwinbox",
    "chargebee",
    "hasura",
    "juspay",
    "cashfree",
    "scaler",
    "browserstack",
    "postman",
    "clevertap",
    "moengage",
    # Global
    "dropbox",
    "reddit",
    "lyft",
    "robinhood",
    "coinbase",
    "brex",
    "rippling",
    "lattice",
    "deel",
    "remote",
    "gusto",
    "loom",
    "notion",
    "retool",
    "airtable",
    "figma",
    "miro",
    "canva",
    "hubspot",
    "intercom",
    "segment",
    "mixpanel",
    "amplitude",
    "contentful",
    "twilio",
    "sendgrid",
    "pagerduty",
    "fastly",
    "cloudinary",
    "algolia",
    "auth0",
    "okta",
    "zendesk",
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
