from .db import init_db, insert_jobs, start_crawl_run, finish_crawl_run
from .sources import remoteok


SOURCES = {
    "remoteok": remoteok.fetch,
}


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
