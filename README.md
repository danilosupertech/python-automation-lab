# Python Automation Lab

Practical Python automations focused on real-world tasks: file processing, data cleaning, API integrations, and reporting.

## Why this repo
This repository showcases production-minded scripting:
- clear folder structure
- repeatable runs
- logging and error handling
- small, focused deliverables

## Projects
### 01 — Bill Organizer
Organizes invoices/documents into a clean folder structure by period and provider.

**Highlights**
- Pathlib-based file handling
- Safe renaming rules
- Logging + dry-run mode

### 02 — CSV Cleaner
Cleans messy CSV files and outputs normalized datasets + a quality report.

**Highlights**
- CLI with arguments
- Data normalization rules
- Summary metrics

### 03 — API Report
Fetches data from a public API and generates a report (CSV/JSON + Markdown/HTML).

**Highlights**
- API consumption
- Report generation
- Designed for scheduling (cron)

## How to run
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
