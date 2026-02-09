from __future__ import annotations

from pathlib import Path

import duckdb
import rio

from .. import components as comps
from .. import data_models

DB_PATH = Path(__file__).parent.parent.parent / "loader" / "remoteok_loader.duckdb"


@rio.page(
    name="Jobs",
    url_segment="",
)
class JobsPage(rio.Component):
    """Page displaying job listings from the DuckDB database."""

    def _load_jobs(self) -> list[data_models.JobListing]:
        conn = duckdb.connect(str(DB_PATH), read_only=True)
        cursor = conn.execute(
            "SELECT job_id, position, company, location, salary_min, salary_max, date, url, tags "
            "FROM job_listings.jobs_with_tags ORDER BY date DESC"
        )
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        return [data_models.JobListing(**dict(zip(columns, row))) for row in rows]

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
