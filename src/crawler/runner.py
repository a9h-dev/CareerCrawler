import json
from pathlib import Path

from .db import init_db, insert_jobs, start_crawl_run, finish_crawl_run, get_jobs
from .sources import remoteok, hackernews, remotive, jobicy, themuse, wellfound, lever, greenhouse


SOURCES = {
    "remoteok": remoteok.fetch,
    "hackernews": hackernews.fetch,
    "remotive": remotive.fetch,
    "jobicy": jobicy.fetch,
    "themuse": themuse.fetch,
    "wellfound": wellfound.fetch,
    "lever": lever.fetch,
    "greenhouse": greenhouse.fetch,
}


def export_json() -> None:
    jobs = get_jobs(active_only=True, limit=10000)
    data = [dict(row) for row in jobs]
    Path("data/jobs.json").write_text(json.dumps(data, indent=2))
    print(f"Exported {len(data)} jobs to data/jobs.json")


def run_all() -> None:
    init_db()

    for source_name, fetch_fn in SOURCES.items():
        run_id = start_crawl_run(source_name)
        try:
            jobs = fetch_fn()
            new_count = insert_jobs(jobs)
            finish_crawl_run(run_id, len(jobs), new_count)
            print(f"{source_name}: {new_count} new jobs out of {len(jobs)}")
        except Exception as e:
            finish_crawl_run(run_id, 0, 0, status="error", error_msg=str(e))
            print(f"{source_name}: FAILED — {e}")

    export_json()
