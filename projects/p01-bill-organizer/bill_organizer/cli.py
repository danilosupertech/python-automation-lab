import argparse
import logging
from pathlib import Path

try:
    from .core import organize
    from .config import DEFAULT_RULES
except ImportError:  # pragma: no cover - fallback for running as a script
    from pathlib import Path as _Path
    import sys as _sys

    _sys.path.append(str(_Path(__file__).resolve().parent.parent))
    from bill_organizer.core import organize  # type: ignore
    from bill_organizer.config import DEFAULT_RULES  # type: ignore

def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser.

    Supported arguments:
        --input/-i: input folder with PDFs.
        --output/-o: output folder where files will be organized.
        --mode: operation mode (copy/move).
        --dry-run: simulate execution without changing files.
        --log-level: log level shown in the console.

    Returns:
        argparse.ArgumentParser: parser with all options supported by the app.
    """
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
    """CLI entry point.

    Args:
        argv (list[str] | None): list of arguments to parse. When None, uses the
            command-line arguments (sys.argv).

    Returns:
        int: exit code (0 on success, 2 when the input folder does not exist).
    """
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
    # Run the application as a script, returning the appropriate exit code.
    raise SystemExit(main())
