import json
import logging
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Tuple

from .config import DEFAULT_RULES, Rules

MONTH_RE = re.compile(r"(20\d{2})[-_](0[1-9]|1[0-2])")
SAFE_RE = re.compile(r"[^a-z0-9]+")


@dataclass
class Result:
    """Agregação de contadores e totais por fornecedor de uma execução.

    Aggregated counters and per-supplier totals for an organize run.
    """
    moved: int = 0
    copied: int = 0
    skipped: int = 0
    errors: int = 0
    by_supplier: Dict[str, int] = None

    def __post_init__(self) -> None:
        if self.by_supplier is None:
            self.by_supplier = {}


def extract_month(filename: str) -> str:
    """Extrai YYYY-MM do nome do arquivo. Padrão 'unknown-month' se não encontrado.
    Aceita padrões como 2026-01 ou 2026_01.

    Extract YYYY-MM from filename. Defaults to 'unknown-month' if not found.
    Accepts patterns like 2026-01 or 2026_01.
    """
    m = MONTH_RE.search(filename)
    if not m:
        return "unknown-month"
    return f"{m.group(1)}-{m.group(2)}"


def slugify(text: str) -> str:
    """Cria um token seguro para nome de arquivo: minúscula, apenas alfanumérico/underscore.

    Create a safe filename token: lowercase, alnum/underscore only.
    """
    t = text.lower()
    t = SAFE_RE.sub("_", t).strip("_")
    return t or "file"


def is_pdf(path: Path) -> bool:
    """Verifica se o caminho é um arquivo PDF.

    Check if the path is a PDF file.
    """
    return path.is_file() and path.suffix.lower() == ".pdf"


def classify(filename: str, rules: Rules) -> str:
    """Classifica um arquivo de acordo com as palavras-chave das regras.

    Classify a file according to the keyword rules for suppliers.

    Args:
        filename: Nome do arquivo a classificar.
        rules: Regras de classificação (keywords por fornecedor).

    Returns:
        str: Nome do fornecedor ou 'outros' se não encontrar correspondência.
    """
    lower = filename.lower()
    for supplier, keywords in rules.suppliers.items():
        if supplier == "outros":
            continue
        for kw in keywords:
            if kw.lower() in lower:
                return supplier
    return "outros"


def iter_pdfs(input_dir: Path) -> Iterable[Path]:
    """Itera sobre todos os arquivos PDF em um diretório.

    Iterate over all PDF files in a directory.

    Args:
        input_dir: Diretório a verificar.

    Yields:
        Path: Caminho para cada arquivo PDF encontrado.
    """
    for p in input_dir.iterdir():
        if is_pdf(p):
            yield p


def ensure_dir(path: Path) -> None:
    """Garante que o diretório existe, criando-o se necessário.

    Ensure that the directory exists, creating it if necessary.

    Args:
        path: Caminho do diretório a criar.
    """
    path.mkdir(parents=True, exist_ok=True)


def transfer_file(src: Path, dst: Path, mode: str, dry_run: bool) -> None:
    """Transfere arquivo (cópia ou movimentação).

    Transfer file (copy or move).

    Args:
        src: Caminho do arquivo de origem.
        dst: Caminho do arquivo de destino.
        mode: Modo de transferência ('copy' ou 'move').
        dry_run: Se True, não faz alterações.

    Raises:
        ValueError: Se o modo não for 'copy' ou 'move'.
    """
    if dry_run:
        return
    if mode == "move":
        shutil.move(str(src), str(dst))
    elif mode == "copy":
        shutil.copy2(str(src), str(dst))
    else:
        raise ValueError(f"Invalid mode: {mode}")


def _compute_target_path(pdf: Path, output_dir: Path, rules: Rules) -> Tuple[Path, str]:
    """Calcula o caminho de destino e o fornecedor para um PDF.

    Compute the target path and supplier for a PDF.

    Args:
        pdf: Caminho do arquivo PDF.
        output_dir: Diretório base de saída.
        rules: Regras de classificação.

    Returns:
        Tuple[Path, str]: Caminho de destino e nome do fornecedor.
    """
    supplier = classify(pdf.name, rules)
    month = extract_month(pdf.name)
    supplier_dir = output_dir / month / supplier
    ensure_dir(supplier_dir)

    stem = Path(pdf.name).stem
    stem_clean = re.sub(rf"^{re.escape(month)}[-_]+", "", stem)
    stem_clean = re.sub(r"^(20\d{2})[-_](0[1-9]|1[0-2])[-_]+", "", stem_clean)
    base = slugify(stem_clean)
    
    prefix = f"{supplier}_"
    if base.startswith(prefix):
        base = base[len(prefix):] or "file"

    new_name_base = f"{month}_{supplier}_{base}"

    n = 1
    while True:
        candidate = supplier_dir / f"{new_name_base}_{n:03d}{pdf.suffix.lower()}"
        if not candidate.exists():
            return candidate, supplier
        n += 1


def organize(
    input_dir: Path,
    output_dir: Path,
    mode: str = "copy",
    dry_run: bool = False,
    rules: Rules = DEFAULT_RULES,
) -> Tuple[Result, Path]:
    """Organiza arquivos PDF em subpastas por fornecedor e mês.

    Organize PDF files into subfolders by supplier and month.

    Args:
        input_dir: Diretório contendo PDFs a organizar.
        output_dir: Diretório base para saída organizada.
        mode: Modo de operação ('copy' ou 'move'). Padrão 'copy'.
        dry_run: Se True, apenas registra sem fazer alterações. Padrão False.
        rules: Regras de classificação por fornecedor. Padrão DEFAULT_RULES.

    Returns:
        Tuple[Result, Path]: Contadores de operação e caminho do arquivo summary.json.
    """
    logger = logging.getLogger("bill_organizer")
    ensure_dir(output_dir)

    result = Result()

    for pdf in iter_pdfs(input_dir):
        try:
            target, supplier = _compute_target_path(pdf, output_dir, rules)
            transfer_file(pdf, target, mode=mode, dry_run=dry_run)

            if not dry_run:
                if mode == "move":
                    result.moved += 1
                else:
                    result.copied += 1
                result.by_supplier[supplier] = result.by_supplier.get(supplier, 0) + 1

            logger.info("%s: %s -> %s", mode.upper(), pdf.name, target)

        except (OSError, ValueError) as exc:
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
