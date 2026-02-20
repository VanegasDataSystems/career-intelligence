# UI Folder

A Rio UI web application built with Python 3.13 for searching and browsing job listings.

## Folder Structure

- `ui/` - Main application module
  - `__init__.py` - App configuration, theme, and rio.App instance
  - `data_models.py` - Data models (`SearchJobResult`, `SkillHighlight`, `SearchResponse`)
  - `components/` - Reusable UI components (export new components in `__init__.py`)
    - `search_bar.py` - Search input with Enter and button submit; uses `on_change` to track text
    - `job_card.py` - `SearchJobCard`: displays title, company, description
    - `skill_chip.py` - Chip badge for a skill with relevance score
    - `ai_summary_placeholder.py` - Card placeholder for AI-generated summary text
  - `pages/` - Page components with `@rio.page` decorator
    - `jobs_page.py` - Main search page (root URL); loads JSON at module level, renders results via dropdown selection
    - `about_page.py` - Simple about page

## Data Flow

Pre-computed pipeline outputs (JSON files in project root) are loaded once at module startup:

1. `search_results_jobs.json` — list of `{search_id, role_query, jobs[]}` entries
2. `search_results_skills.json` — list of `{search_id, skills[]}` entries
3. `jobs_cleaned_with_skills.json` — cleaned job records with `description_clean` and `skills[]`

On role selection (`_on_select`):
1. User picks a `role_query` from the dropdown (exact match, no scoring logic)
2. `SearchJobResult` list built, enriched with `description` and `skills` from cleaned data
3. `SkillHighlight` list built from matched skills entry
4. `SearchResponse` stored in component state; `build()` re-renders

**No database access in the UI layer.** All data comes from JSON files.

## RAG Flow Integration Plan

### Current State (known)

The `llm/` module (`llm-v1` branch) is a **CLI script**, not an HTTP service:
- `llm/run.py` reads the last entry from `search_results_jobs.json` + `search_results_skills.json`
- Calls `generate_explanation(role_query, skills, jobs)` in `llm/model.py`
- `model.py` loads TinyLlama from `models/tiny-llama/` via HuggingFace `transformers`
- Writes output to `final_results.json`

**Known response shape** (from `final_results.json`):
```
{
  "search_id": 5,
  "role_query": "software engineer",
  "location_filter": "",
  "jobs": [ ... ],
  "skills": [ ... ],
  "ai_summary": "Generated paragraph text..."
}
```

This maps directly onto `SearchResponse` — the data model is already aligned.

**UI scaffolding already in place:**
- `SearchResponse.ai_summary: str` field ready to receive text
- `AiSummaryPlaceholder(summary_text=...)` renders whatever string is passed
- `search_bar.py` exists and works — ready to replace the dropdown when backend is live

### What Requires RAG Inspection

Before wiring the UI to the backend, confirm:

1. **HTTP interface** — Does `llm/run.py` get wrapped in a FastAPI/Flask endpoint, or called as a subprocess? Need the URL, method, and request body shape.
2. **Request format** — Does the endpoint accept `{"query": "trading engineer"}` or something else?
3. **Response format** — Confirm it matches the known `final_results.json` shape above, or document any differences.
4. **Synchronous vs. streaming** — TinyLlama generation is slow (~5–30s). Is the response returned all at once, or streamed token-by-token? Streaming would require `rio` async handling.
5. **Error responses** — What does the endpoint return on failure (bad query, model not loaded, timeout)?

### UI Changes When Backend Is Ready

1. **Replace dropdown with `SearchBar`** — swap `rio.Dropdown` back to `comps.SearchBar` in `jobs_page.py`
2. **Add loading state** — new `is_loading: bool` attribute on `JobsPage`; show a spinner while awaiting response
3. **Call the endpoint** — in `_on_search()`, POST the query via `httpx` or `aiohttp`; parse JSON response into `SearchResponse`
4. **Render `ai_summary`** — pass `self.search_results.ai_summary` to `AiSummaryPlaceholder(summary_text=...)`
5. **Handle errors** — show an error message if the endpoint is unreachable or returns non-200

### To Test LLM Locally (CLI, no endpoint)

```bash
git checkout origin/llm-v1 -- llm/
uv pip install torch transformers accelerate
# Download TinyLlama model (~2GB) to models/tiny-llama/
python -m llm.run
# Output written to final_results.json
```

Machine has RTX 4060 Ti (16GB VRAM) — TinyLlama runs fully GPU-accelerated.

## Development

### Run Development Server

```bash
uv run rio run
```

Hot reload is active — no restart needed after file changes.

### Run Data Loader (pipeline, not needed for UI)

```bash
uv run python loader/remoteok_loader.py
uv run python loader/create_views.py
```

## Rio Patterns

### Pages
- Use `@rio.page(name="Page Name", url_segment="url-path")` decorator
- Use `url_segment=""` for the root/home page
- Inherit from `rio.Component` and implement `build()` method

### Components
- Inherit from `rio.Component`; define attributes as class variables
- Implement `build()` returning a `rio.Component`
- Export new components in `ui/components/__init__.py`
- Use `self.bind().attr` for two-way TextInput binding; also add `on_change` handler to capture text reliably before confirm/click events fire

### Common Rio Components
- `rio.Column`, `rio.Row` — layout with `spacing`, `margin`
- `rio.Card` — card container with `margin_bottom`
- `rio.Text` — text with `style` (`"heading1"`, `"heading2"`, `"heading3"`, or `rio.TextStyle`)
- `rio.TextInput` — text field with `on_confirm`, `on_change`, `text=self.bind().attr`
- `rio.Button` — button with `on_press`
- `rio.FlowContainer` — wrapping chip layout with `row_spacing`, `column_spacing`
- `rio.Separator` — horizontal rule
- `rio.Spacer` — flexible space filler
- `rio.Link` — link with `target_url` and `open_in_new_tab`

## Tech Stack

- **Framework**: [Rio UI](https://rio.dev) (v0.12+)
- **Data Pipeline**: dlt + DuckDB (loader layer, separate from UI)
- **Package Manager**: uv
- **Python**: 3.13
