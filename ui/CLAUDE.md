# UI Folder

A Rio UI web application built with Python 3.13.

## Folder Structure

- `ui/` - Main application module
  - `__init__.py` - App configuration, theme, and rio.App instance
  - `data_models.py` - Data models (dataclasses and rio.UserSettings)
  - `components/` - Reusable UI components (export new components in `__init__.py`)
  - `pages/` - Page components with `@rio.page` decorator
- `loader/` - Data loading pipelines
  - `remoteok_loader.py` - dlt pipeline for RemoteOK job listings
  - `remoteok_loader.duckdb` - DuckDB database with loaded data
  - `create_views.py` - Script to create/update database views
  - `sql/` - SQL files for views and queries

## Development

### Setup

```bash
uv sync
```

### Run Development Server

```bash
uv run rio run
```

### Run Data Loader

```bash
uv run python loader/remoteok_loader.py
```

### Create/Update Database Views

```bash
uv run python loader/create_views.py
```

## Rio Patterns

### Pages
- Use `@rio.page(name="Page Name", url_segment="url-path")` decorator
- Inherit from `rio.Component` and implement `build()` method
- Access session data via `self.session`

### Components
- Inherit from `rio.Component`
- Define attributes as class variables (rio handles state)
- Implement `build()` method returning a `rio.Component`
- Export new components in `ui/components/__init__.py`

### Common Rio Components
- `rio.Column`, `rio.Row` - Layout containers with `spacing`, `margin`
- `rio.Card` - Card container
- `rio.Text` - Text with `style` (e.g., "heading1", "heading2", or `rio.TextStyle`)
- `rio.Link` - Links with `target_url` and `open_in_new_tab`
- `rio.Spacer` - Flexible space filler

## Database Schema

The DuckDB database (`loader/remoteok_loader.duckdb`) contains:
- `job_listings.remoteok_jobs` - Main jobs table with `_dlt_id` as internal ID
- `job_listings.remoteok_jobs__tags` - Tags table with `_dlt_parent_id` foreign key
- `job_listings.jobs_with_tags` - View joining jobs with aggregated tags

## Tech Stack

- **Framework**: [Rio UI](https://rio.dev) (v0.12+)
- **Data Pipeline**: dlt (data load tool)
- **Database**: DuckDB
- **Package Manager**: uv
- **Python**: 3.13
