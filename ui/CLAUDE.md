# UI Folder

A Rio UI web application built with Python 3.13 for browsing job listings.

## Folder Structure

- `ui/` - Main application module
  - `__init__.py` - App configuration, theme, and rio.App instance
  - `data_models.py` - Data models (dataclasses with `__post_init__` for type conversion)
  - `components/` - Reusable UI components (export new components in `__init__.py`)
    - `job_card.py` - Card component displaying a single job listing
  - `pages/` - Page components with `@rio.page` decorator
    - `jobs_page.py` - Main page listing all jobs (root URL)
    - `about_page.py` - Simple about page
- `loader/` - Data loading pipelines
  - `remoteok_loader.py` - dlt pipeline for RemoteOK job listings
  - `remoteok_loader.duckdb` - DuckDB database with loaded data
  - `create_views.py` - Script to create/update database views
  - `sql/` - SQL files for views and queries

## Data Flow

1. **Load**: `loader/remoteok_loader.py` fetches jobs from RemoteOK API via dlt pipeline
2. **Store**: Data stored in DuckDB with schema `job_listings`
3. **View**: `loader/create_views.py` creates `jobs_with_tags` view joining jobs with tags
4. **Query**: `jobs_page.py` queries DuckDB using cursor description for column names
5. **Convert**: Results converted to dicts via `zip(columns, row)` and unpacked into `JobListing(**row)`
6. **Normalize**: `JobListing.__post_init__` handles type conversions (None -> "", dates -> str)
7. **Render**: `JobCard` component displays each listing

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

### Navigation
- Rio auto-generates sidebar navigation when multiple pages exist
- Each `@rio.page` decorator adds a navigation link

### Pages
- Use `@rio.page(name="Page Name", url_segment="url-path")` decorator
- Use `url_segment=""` for the root/home page
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
