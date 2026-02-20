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


# Load pre-computed pipeline outputs once at module level
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

# Available role queries directly from the pre-computed results
_ROLE_QUERIES: list[str] = [entry["role_query"] for entry in _SEARCH_JOBS]

# Direct lookup: role_query -> (jobs_entry, skills_entry)
_SKILLS_BY_SEARCH_ID: dict[int, dict] = {
    s["search_id"]: s for s in _SEARCH_SKILLS
}


def _load_results(role_query: str) -> data_models.SearchResponse:
    """Build a SearchResponse directly from pre-computed JSON for the given role_query."""
    jobs_entry = next(e for e in _SEARCH_JOBS if e["role_query"] == role_query)
    skills_entry = _SKILLS_BY_SEARCH_ID.get(jobs_entry["search_id"])

    jobs = []
    for j in jobs_entry["jobs"]:
        job_id = str(j["job_id"])
        jobs.append(
            data_models.SearchJobResult(
                job_id=job_id,
                title=j["title"],
                company=j.get("company", ""),
                location=j.get("location", ""),
                score=j["score"],
                url=j["url"],
                skills=_SKILLS_BY_JOB.get(job_id, []),
                description=_DESCRIPTION_BY_JOB.get(job_id, ""),
            )
        )

    skill_highlights = [
        data_models.SkillHighlight(name=s["name"], score=s["score"])
        for s in (skills_entry["skills"] if skills_entry else [])
    ]

    return data_models.SearchResponse(
        query=role_query,
        jobs=jobs,
        skills=skill_highlights,
    )


@rio.page(
    name="Jobs",
    url_segment="",
)
class JobsPage(rio.Component):
    """Page displaying pre-computed job search results selected from a dropdown."""

    selected_query: str | None = None
    search_results: data_models.SearchResponse | None = None

    def _on_select(self, event: rio.DropdownChangeEvent) -> None:
        self.selected_query = event.value
        self.search_results = _load_results(event.value)

    def build(self) -> rio.Component:
        desktop_layout = self.session.window_width > 40

        sections: list[rio.Component] = [
            rio.Dropdown(
                options=_ROLE_QUERIES,
                selected_value=self.selected_query,
                label="Select a role...",
                on_change=self._on_select,
                grow_x=True,
            ),
        ]

        if self.search_results is None:
            sections.append(
                rio.Text(
                    "Select a role above to see results.",
                    style=rio.TextStyle(italic=True, fill=rio.Color.from_hex("888888")),
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
                sections.append(rio.Text("Skill Highlights", style="heading2"))
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

            # Job results
            sections.append(rio.Text("Job Results", style="heading2"))
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
