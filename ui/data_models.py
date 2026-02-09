from __future__ import annotations

import dataclasses
from typing import Any


@dataclasses.dataclass
class JobListing:
    job_id: Any
    position: Any
    company: Any
    location: Any
    salary_min: int | None
    salary_max: int | None
    date: Any
    url: Any
    tags: Any

    def __post_init__(self) -> None:
        self.job_id = str(self.job_id) if self.job_id else ""
        self.position = self.position or ""
        self.company = self.company or ""
        self.location = self.location or ""
        self.date = str(self.date) if self.date else ""
        self.url = self.url or ""
        self.tags = self.tags or ""