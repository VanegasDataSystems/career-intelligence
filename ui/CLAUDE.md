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

## LLM Integration (pending)

- `SearchResponse.ai_summary` field is ready to receive generated text
- `AiSummaryPlaceholder` accepts `summary_text` param — wire in once the LLM endpoint is available
- The `llm/` module (`llm-v1` branch) uses TinyLlama via HuggingFace `transformers`
- To test locally: `git checkout origin/llm-v1 -- llm/` then `python -m llm.run`
- Requires: `torch`, `transformers`, `accelerate` and model at `models/tiny-llama/`

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
