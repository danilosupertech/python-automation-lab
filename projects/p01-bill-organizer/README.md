# P01 — Bill Organizer (MVP)

Organize **PDF bills** into folders by supplier and month, with automatic classification and summary generation.

## Features

- **Automatic Classification**: Classifies PDFs by supplier using filename keywords
- **Month-Based Organization**: Organizes files into folders by month (YYYY-MM)
- **Flexible File Transfer**: Copy or move files to the output directory
- **Safe Renaming**: Generates unique, safe filenames with automatic conflict resolution
- **Summary Report**: Generates `summary.json` with operation statistics and per-supplier counts
- **Dry-Run Mode**: Preview changes without modifying any files
- **Detailed Logging**: Configurable log levels for debugging

## How It Works

1. Scans the input folder for PDF files
2. Extracts the month from the filename (e.g., `2026-01` from `2026-01_EDP_fatura.pdf`)
3. Classifies the supplier based on keywords in the filename
4. Organizes files into: `output/<YYYY-MM>/<supplier>/`
5. Renames files safely with format: `<YYYY-MM>_<supplier>_<name>_001.pdf`
6. Generates a summary with operation statistics

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Basic copy operation
```bash
python -m bill_organizer --input data --output output --mode copy
```

### Move files instead of copying
```bash
python -m bill_organizer --input data --output output --mode move
```

### Preview changes without modifying files
```bash
python -m bill_organizer --input data --output output --dry-run
```

### Adjust log level
```bash
python -m bill_organizer --input data --output output --log-level DEBUG
```

### All available options
```bash
python -m bill_organizer --help
```

## Example

### Input
Place PDFs in `data/` folder:
- `2026-01_EDP_fatura.pdf`
- `2026-01_MEO_internet.pdf`
- `2026-01_Aguas_conta.pdf`

### Output Structure
```
output/
├── 2026-01/
│   ├── edp/
│   │   └── 2026-01_edp_fatura_001.pdf
│   ├── meo/
│   │   └── 2026-01_meo_internet_001.pdf
│   ├── aguas/
│   │   └── 2026-01_aguas_conta_001.pdf
│   └── outros/
└── summary.json
```

### Summary Report
```json
{
  "mode": "copy",
  "dry_run": false,
  "moved": 0,
  "copied": 3,
  "skipped": 0,
  "errors": 0,
  "by_supplier": {
    "edp": 1,
    "meo": 1,
    "aguas": 1
  }
}
```

## Configuration

Suppliers and their keywords are defined in `bill_organizer/config.py`. Customize them to match your billing systems.

## Supported Arguments

| Argument | Short | Default | Description |
|----------|-------|---------|-------------|
| `--input` | `-i` | `data` | Input folder with PDFs |
| `--output` | `-o` | `output` | Output folder for organized files |
| `--mode` | - | `copy` | Operation mode: `copy` or `move` |
| `--dry-run` | - | False | Simulate without changing files |
| `--log-level` | - | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR |

## Project Structure

```
bill_organizer/
├── __init__.py
├── __main__.py      # Entry point for `python -m bill_organizer`
├── cli.py           # Command-line interface
├── config.py        # Supplier keywords configuration
├── core.py          # Core logic for file organization
└── __pycache__/
```

## License

MIT
