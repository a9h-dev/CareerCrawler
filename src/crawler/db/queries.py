from __future__ import annotations

import sqlite3
from dataclasses import asdict
from typing import Optional

from .connection import get_connection
from ..models import Job


# ── Jobs ──────────────────────────────────────────────────────────────────────

def insert_job(job: Job) -> bool:
    """Returns True if the job was newly inserted (not a duplicate)."""
    sql = """
        INSERT OR IGNORE INTO jobs (url, title, company, location, salary, source, posted_at)
        VALUES (:url, :title, :company, :location, :salary, :source, :posted_at)
    """
    with get_connection() as conn:
        cursor = conn.execute(sql, asdict(job))
        return cursor.rowcount == 1


def insert_jobs(jobs: list[Job]) -> int:
    """Bulk insert, returns count of newly inserted rows."""
    return sum(insert_job(j) for j in jobs)


def get_jobs(
    source: Optional[str] = None,
    active_only: bool = True,
    limit: int = 100,
) -> list[sqlite3.Row]:
    where_clauses = []
    params: dict = {}

    if active_only:
        where_clauses.append("is_active = 1")
    if source:
        where_clauses.append("source = :source")
        params["source"] = source

    where = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
    params["limit"] = limit

    sql = f"SELECT * FROM jobs {where} ORDER BY crawled_at DESC LIMIT :limit"

    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()


def mark_inactive(url: str) -> None:
    with get_connection() as conn:
        conn.execute("UPDATE jobs SET is_active = 0 WHERE url = :url", {"url": url})


# ── Crawl runs ────────────────────────────────────────────────────────────────

def start_crawl_run(source: str) -> int:
    sql = "INSERT INTO crawl_runs (source) VALUES (:source)"
    with get_connection() as conn:
        cursor = conn.execute(sql, {"source": source})
        return cursor.lastrowid


def finish_crawl_run(
    run_id: int,
    jobs_found: int,
    jobs_new: int,
    status: str = "success",
    error_msg: Optional[str] = None,
) -> None:
    sql = """
        UPDATE crawl_runs
        SET finished_at = datetime('now'),
            jobs_found  = :jobs_found,
            jobs_new    = :jobs_new,
            status      = :status,
            error_msg   = :error_msg
        WHERE id = :id
    """
    with get_connection() as conn:
        conn.execute(sql, {
            "id": run_id,
            "jobs_found": jobs_found,
            "jobs_new": jobs_new,
            "status": status,
            "error_msg": error_msg,
        })
