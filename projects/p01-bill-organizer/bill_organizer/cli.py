import argparse
import logging
from pathlib import Path

from .core import organize
from .config import DEFAULT_RULES

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="bill_organizer",
        description="Organize PDF bills by supplier using filename matching (MVP).",
    )
    p.add_argument("--input", "-i", default="data", help="Input folder containing PDFs.")
    p.add_argument("--output", "-o", default="output", help="Output folder.")
    p.add_argument("--mode", choices=["copy", "move"], default="copy", help="Copy or move files.")
    p.add_argument("--dry-run", action="store_true", help="No changes; only logs.")
    p.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return p

def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s - %(message)s")

    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()

    if not input_dir.exists():
        logging.error("Input folder does not exist: %s", input_dir)
        return 2

    result, summary_path = organize(
        input_dir=input_dir,
        output_dir=output_dir,
        mode=args.mode,
        dry_run=args.dry_run,
        rules=DEFAULT_RULES,
    )

    logging.info("Done. moved=%d copied=%d skipped=%d errors=%d",
                 result.moved, result.copied, result.skipped, result.errors)

    if not args.dry_run:
        logging.info("Summary: %s", summary_path)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
