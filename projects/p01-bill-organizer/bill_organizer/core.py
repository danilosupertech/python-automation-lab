import json
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

from .config import Rules, DEFAULT_RULES

@dataclass
class Result:
    moved: int = 0
    copied: int = 0
    skipped: int = 0
    errors: int = 0
    by_supplier: Dict[str, int] = None

    def __post_init__(self) -> None:
        if self.by_supplier is None:
            self.by_supplier = {}

def is_pdf(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".pdf"

def classify(filename: str, rules: Rules) -> str:
    lower = filename.lower()
    for supplier, keywords in rules.suppliers.items():
        if supplier == "outros":
            continue
        for kw in keywords:
            if kw.lower() in lower:
                return supplier
    return "outros"

def iter_pdfs(input_dir: Path) -> Iterable[Path]:
    for p in input_dir.iterdir():
        if is_pdf(p):
            yield p

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def transfer_file(src: Path, dst: Path, mode: str, dry_run: bool) -> None:
    if dry_run:
        return
    if mode == "move":
        shutil.move(str(src), str(dst))
    elif mode == "copy":
        shutil.copy2(str(src), str(dst))
    else:
        raise ValueError(f"Invalid mode: {mode}")

def organize(
    input_dir: Path,
    output_dir: Path,
    mode: str = "copy",
    dry_run: bool = False,
    rules: Rules = DEFAULT_RULES,
) -> Tuple[Result, Path]:
    logger = logging.getLogger("bill_organizer")
    ensure_dir(output_dir)

    result = Result()

    for pdf in iter_pdfs(input_dir):
        try:
            supplier = classify(pdf.name, rules)
            supplier_dir = output_dir / supplier
            ensure_dir(supplier_dir)

            target = supplier_dir / pdf.name
            if target.exists():
                result.skipped += 1
                logger.info("SKIP (exists): %s -> %s", pdf.name, target)
                continue

            transfer_file(pdf, target, mode=mode, dry_run=dry_run)

            if mode == "move":
                result.moved += 1
            else:
                result.copied += 1

            result.by_supplier[supplier] = result.by_supplier.get(supplier, 0) + 1
            logger.info("%s: %s -> %s", mode.upper(), pdf.name, target)

        except Exception as exc:
            result.errors += 1
            logger.exception("ERROR processing %s: %s", pdf, exc)

    summary_path = output_dir / "summary.json"
    if not dry_run:
        summary_path.write_text(
            json.dumps(
                {
                    "mode": mode,
                    "dry_run": dry_run,
                    "moved": result.moved,
                    "copied": result.copied,
                    "skipped": result.skipped,
                    "errors": result.errors,
                    "by_supplier": result.by_supplier,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
            newline="\n",
        )

    return result, summary_path
