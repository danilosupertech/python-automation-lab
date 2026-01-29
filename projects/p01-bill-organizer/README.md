# P01 — Bill Organizer (MVP)

Organize **PDF bills** into folders by supplier and month, with automatic classification and summary generation.

[![Tests](https://img.shields.io/badge/tests-63%20passed-success)](tests/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![Code Style](https://img.shields.io/badge/code%20style-documented-brightgreen)]()

## Features

- **Automatic Classification**: Classifies PDFs by supplier using filename keywords
- **Month-Based Organization**: Organizes files into folders by month (YYYY-MM)
- **Flexible File Transfer**: Copy or move files to the output directory
- **Safe Renaming**: Generates unique, safe filenames with automatic conflict resolution
- **Summary Report**: Generates `summary.json` with operation statistics and per-supplier counts
- **Dry-Run Mode**: Preview changes without modifying any files
- **Detailed Logging**: Configurable log levels for debugging
- **Fully Tested**: 63 unit tests covering all functionality
- **Bilingual Documentation**: Code documented in Portuguese and English

## How It Works

1. Scans the input folder for PDF files
2. Extracts the month from the filename (e.g., `2026-01` from `2026-01_EDP_fatura.pdf`)
3. Classifies the supplier based on keywords in the filename
4. Organizes files into: `output/<YYYY-MM>/<supplier>/`
5. Renames files safely with format: `<YYYY-MM>_<supplier>_<name>_001.pdf`
6. Generates a summary with operation statistics

## Installation

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
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

**Default Suppliers:**
- **edp**: energia, electricidade
- **meo**: telecom, fibra, internet
- **aguas**: água, águas, smas
- **condominio**: condomínio, quota, admin
- **outros**: unmatched files

## Testing

The project includes a comprehensive test suite with 63 tests covering all functionality.

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage report
```bash
pytest tests/ --cov=bill_organizer --cov-report=term-missing
```

### Run specific test file
```bash
pytest tests/test_core.py -v
pytest tests/test_cli.py -v
```

### Test Structure
- `tests/test_core.py`: Tests for core business logic (50 tests)
  - File classification and organization
  - Month extraction and slugification
  - File transfer operations
  - Path computation
- `tests/test_cli.py`: Tests for CLI interface (13 tests)
  - Argument parsing
  - Main entry point
  - Configuration handling

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
└── core.py          # Core logic for file organization

tests/
├── __init__.py
├── test_cli.py      # CLI tests (13 tests)
└── test_core.py     # Core logic tests (50 tests)

data/                # Input folder (place your PDFs here)
output/              # Output folder (organized files)
examples/            # Example usage
requirements.txt     # Python dependencies
```

## Code Quality

- **Documented Code**: All functions have bilingual docstrings (Portuguese/English)
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Specific exception handling (OSError, ValueError)
- **Tested**: 63 unit tests with edge cases and error scenarios
- **Clean Code**: Refactored to minimize complexity (reduced from 21 to <15 local variables per function)

## Dependencies

### Runtime
- Python 3.8+
- Standard library only (no external runtime dependencies)

### Development
- pytest >= 7.0
- pytest-cov >= 4.0

## Development

### Install development dependencies
```bash
pip install pytest pytest-cov
```

### Run linting
```bash
pylint bill_organizer/
```

### Format code
```bash
black bill_organizer/
```

## License

MIT
