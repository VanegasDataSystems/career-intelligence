from __future__ import annotations

import json
from pathlib import Path

import rio

from .. import components as comps
from .. import data_models

DATA_DIR = Path(__file__).parent.parent.parent


def _load_json(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    with open(path) as f:
        return json.load(f)


# Load data once at module level
_SEARCH_JOBS: list[dict] = _load_json("search_results_jobs.json")
_SEARCH_SKILLS: list[dict] = _load_json("search_results_skills.json")
_JOBS_WITH_SKILLS: list[dict] = _load_json("jobs_cleaned_with_skills.json")

# Build lookups from the cleaned jobs data
_SKILLS_BY_JOB: dict[str, list[str]] = {
    str(j["job_id"]): j.get("skills", []) for j in _JOBS_WITH_SKILLS
}
_DESCRIPTION_BY_JOB: dict[str, str] = {
    str(j["job_id"]): j.get("description_clean", "") for j in _JOBS_WITH_SKILLS
}


def _word_overlap_score(query: str, role_query: str) -> float:
    """Score how well a user query matches a pre-computed role_query using word overlap."""
    query_words = set(query.lower().split())
    role_words = set(role_query.lower().split())
    if not query_words or not role_words:
        return 0.0
    overlap = query_words & role_words
    return len(overlap) / max(len(query_words), len(role_words))


def _find_best_search(query: str) -> tuple[dict | None, dict | None]:
    """Find the best-matching pre-computed search for a query. Returns (jobs_entry, skills_entry)."""
    best_score = 0.0
    best_idx = -1

    for i, entry in enumerate(_SEARCH_JOBS):
        score = _word_overlap_score(query, entry["role_query"])
        if score > best_score:
            best_score = score
            best_idx = i

    if best_idx < 0 or best_score == 0.0:
        return None, None

    jobs_entry = _SEARCH_JOBS[best_idx]
    # Match skills by search_id
    skills_entry = None
    for s in _SEARCH_SKILLS:
        if s["search_id"] == jobs_entry["search_id"]:
            skills_entry = s
            break

    return jobs_entry, skills_entry


@rio.page(
    name="Jobs",
    url_segment="",
)
class JobsPage(rio.Component):
    """Search-driven page displaying job results from pre-computed JSON data."""

    search_query: str = ""
    search_results: data_models.SearchResponse | None = None
    has_searched: bool = False

    def _on_search(self, query: str) -> None:
        self.search_query = query
        self.has_searched = True

        if not query.strip():
            self.search_results = None
            return

        jobs_entry, skills_entry = _find_best_search(query)

        if jobs_entry is None:
            self.search_results = data_models.SearchResponse(
                query=query, jobs=[], skills=[]
            )
            return

        # Build SearchJobResult list, enriching with skills and description from cleaned data
        jobs = []
        for j in jobs_entry["jobs"]:
            job_id = str(j["job_id"])
            skills = _SKILLS_BY_JOB.get(job_id, [])
            description = _DESCRIPTION_BY_JOB.get(job_id, "")
            jobs.append(
                data_models.SearchJobResult(
                    job_id=job_id,
                    title=j["title"],
                    company=j.get("company", ""),
                    location=j.get("location", ""),
                    score=j["score"],
                    url=j["url"],
                    skills=skills,
                    description=description,
                )
            )

        # Build SkillHighlight list
        skill_highlights = []
        if skills_entry:
            for s in skills_entry["skills"]:
                skill_highlights.append(
                    data_models.SkillHighlight(name=s["name"], score=s["score"])
                )

        self.search_results = data_models.SearchResponse(
            query=query,
            jobs=jobs,
            skills=skill_highlights,
        )

    def build(self) -> rio.Component:
        desktop_layout = self.session.window_width > 40

        sections: list[rio.Component] = [
            comps.SearchBar(
                query=self.search_query,
                on_search=self._on_search,
            ),
        ]

        if not self.has_searched:
            sections.append(
                rio.Text(
                    "Enter a role to search (e.g. trading engineer, manager, hr remote, frontend engineer)",
                    style=rio.TextStyle(
                        italic=True,
                        fill=rio.Color.from_hex("888888"),
                    ),
                    justify="center",
                )
            )
        elif self.search_results is None:
            sections.append(
                rio.Text(
                    "Please enter a search query.",
                    style=rio.TextStyle(italic=True, fill=rio.Color.from_hex("888888")),
                    justify="center",
                )
            )
        elif not self.search_results.jobs:
            sections.append(
                rio.Text(
                    f"No results found for '{self.search_results.query}'. Try: trading engineer, manager, hr remote, frontend engineer",
                    style=rio.TextStyle(italic=True, fill=rio.Color.from_hex("cc0000")),
                    justify="center",
                )
            )
        else:
            # Skill highlights
            if self.search_results.skills:
                skill_chips = [
                    comps.SkillChip(name=s.name, score=s.score)
                    for s in self.search_results.skills
                ]
                sections.append(
                    rio.Text("Skill Highlights", style="heading2"),
                )
                sections.append(
                    rio.FlowContainer(
                        *skill_chips,
                        row_spacing=0.4,
                        column_spacing=0.4,
                    )
                )

            # AI summary
            sections.append(rio.Text("AI Summary", style="heading2"))
            sections.append(comps.AiSummaryPlaceholder())

            # Results header
            sections.append(
                rio.Text("Job Results", style="heading2")
            )

            # Job cards
            for job in self.search_results.jobs:
                sections.append(comps.SearchJobCard(job=job))

        sections.append(rio.Spacer())

        return rio.Column(
            *sections,
            grow_y=True,
            spacing=1,
            margin=1,
            margin_top=2,
            align_x=0.5 if desktop_layout else None,
            min_width=40 if desktop_layout else 0,
        )
