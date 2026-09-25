from src.crawler.scheduler import start_scheduler
import sys

if __name__ == "__main__":
    if "--run-now" in sys.argv:
        from src.crawler.runner import run_all
        run_all()
    else:
        start_scheduler()
