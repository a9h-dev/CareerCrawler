import argparse
from apscheduler.schedulers.blocking import BlockingScheduler
from .runner import run_all


def start_scheduler() -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(run_all, "cron", hour=9, minute=0)
    print("Scheduler started — runs daily at 9:00 AM. Press Ctrl+C to stop.")
    scheduler.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-now", action="store_true")
    args = parser.parse_args()

    if args.run_now:
        run_all()
    else:
        start_scheduler()
