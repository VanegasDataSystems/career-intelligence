# Data Cleaning Summary

This step converts raw job postings from the RemoteOK API into a clean, structured dataset for downstream analysis.

## What was done

* Ingested raw job data from DuckDB (`remoteok_jobs`)
* Cleaned all text fields (title, company, location, description):

  * fixed encoding / mojibake issues
  * removed HTML tags
  * normalized Unicode
  * reduced obvious boilerplate in descriptions
* Output stored as UTF-8 JSON for reliable inspection

## Skill Extraction

* Extracts **explicit technical skills only** (languages, frameworks, tools, platforms)
* Uses a single canonical skill list (`skills.json`)
* Deterministic matching; no keyword or free-text extraction
* Ambiguous terms (e.g. *Go*) require programming context
* Jobs may legitimately have an empty skill list if no technical skills are stated

## Output

Each job includes:

* cleaned job text
* a normalized list of technical skills
* basic metadata (title, company, location, URL)
