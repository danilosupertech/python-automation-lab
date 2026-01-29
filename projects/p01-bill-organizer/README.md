# P01 — Bill Organizer (MVP)

Organize **PDF bills** into folders and generate a quick summary.

## What it does
- Reads PDFs from `data/`
- Classifies by supplier using **filename keywords**
- Copies/moves into `output/<supplier>/`
- Writes `output/summary.json`

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
python -m bill_organizer --input data --output output --mode copy
python -m bill_organizer --input data --output output --mode move --dry-run
```
