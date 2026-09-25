from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    url: str
    title: str
    source: str
    company: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    posted_at: Optional[str] = None
