# Crawler

This contains a web crawler that scrapes job listings and full job descriptions from RemoteOK and stores the results in a DuckDB database.

The crawler is intended to be run locally and can regenerate the database at any time.

## Get the code

Clone the repository and move into it:

git clone `<REPO_URL>`
cd career-intelligence

All commands below assume you are inside the project root directory (career-intelligence).

## Local setup

### Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- Internet access

### Create and activate a virtual environment

From the project root:

Windows (Git Bash):

python -m venv venv source venv/Scripts/activate

macOS / Linux:

python3 -m venv venv source venv/bin/activate

### Install dependencies

pip install playwright duckdb

python -m playwright install chromium

## Database setup (one time)

Before running the crawler for the first time, initialize the DuckDB schema.

From the project root:

python db/init.py

This creates a DuckDB database file named jobs.duckdb in the project root directory.

## Running the crawler

Always run the crawler from the project root, not from inside the crawler folder.

With the virtual environment activated, run:

python -m crawler.main

The crawler will:

- load job listings from RemoteOK
- visit individual job pages - extract full job descriptions
- insert up to 10 jobs into DuckDB (this number is intentional for safety). If more sample data is required, change the counter in crawler/main.py

## Viewing the database contents

The file jobs.duckdb is a binary database file and cannot be opened in a text editor.

To inspect the data, use Python, follow steps below:

From the project root:

python

Then run the following inside Python:

import duckdb conn = duckdb.connect("jobs.duckdb")

List tables: conn.execute("SHOW TABLES").fetchall()

Count rows: conn.execute("SELECT COUNT(\*) FROM jobs").fetchone()

View sample rows: conn.execute("SELECT job_id, title, company FROM jobs LIMIT 5").fetchall()

## Notes

- The 10-job insert limit is intentional for development and testing.
- Job descriptions come from multiple page structures; the crawler handles this automatically.
- The database can be regenerated at any time by re-running the crawler.
