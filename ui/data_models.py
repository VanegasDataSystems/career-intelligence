from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class SearchJobResult:
    job_id: str
    title: str
    company: str
    location: str
    score: float
    url: str
    skills: list[str] = dataclasses.field(default_factory=list)
    description: str = ""


@dataclasses.dataclass
class SkillHighlight:
    name: str
    score: float


@dataclasses.dataclass
class SearchResponse:
    query: str
    jobs: list[SearchJobResult]
    skills: list[SkillHighlight]
    ai_summary: str = ""