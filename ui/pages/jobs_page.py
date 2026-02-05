from __future__ import annotations

from pathlib import Path

import duckdb
import rio

from .. import components as comps
from .. import data_models

DB_PATH = Path(__file__).parent.parent.parent / "loader" / "remoteok_loader.duckdb"


@rio.page(
    name="Jobs",
    url_segment="jobs",
)
class JobsPage(rio.Component):
    """Page displaying job listings from the DuckDB database."""

    def _load_jobs(self) -> list[data_models.JobListing]:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        result = conn.execute(
            "SELECT job_id, position, company, location, salary_min, salary_max, date, url, tags "
            "FROM job_listings.jobs_with_tags ORDER BY date DESC"
        ).fetchall()
        conn.close()

        jobs = []
        for row in result:
            jobs.append(
                data_models.JobListing(
                    job_id=str(row[0]) if row[0] else "",
                    position=row[1] or "",
                    company=row[2] or "",
                    location=row[3] or "",
                    salary_min=row[4],
                    salary_max=row[5],
                    date=str(row[6]) if row[6] else "",
                    url=row[7] or "",
                    tags=row[8] or "",
                )
            )
        return jobs

    def build(self) -> rio.Component:
        jobs = self._load_jobs()

        desktop_layout = self.session.window_width > 40

        return rio.Column(
            rio.Text(
                f"Job Listings ({len(jobs)} jobs)",
                style="heading1",
                justify="center",
            ),
            rio.Column(
                *[comps.JobCard(job=job) for job in jobs],
                rio.Spacer(),
                grow_y=True,
                spacing=0.5,
            ),
            margin=1,
            margin_top=2,
            spacing=1,
            align_x=0.5 if desktop_layout else None,
            min_width=40 if desktop_layout else 0,
        )
