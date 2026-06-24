from __future__ import annotations

from pathlib import Path

DOCUMENT_SUFFIXES = {".md", ".mdx", ".txt", ".pdf", ".docx"}
DATA_SUFFIXES = {".csv", ".json", ".md", ".mdx", ".txt", ".xlsx", ".yml", ".yaml"}
SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}


def relative_path(repo: Path, path: Path) -> str:
    return path.relative_to(repo).as_posix()


def first_existing(repo: Path, candidates: list[str]) -> Path | None:
    for candidate in candidates:
        path = repo / candidate
        if path.exists():
            return path
    return None


def iter_repo_files(repo: Path) -> list[Path]:
    files: list[Path] = []

    for path in repo.rglob("*"):
        if any(part in SKIP_PARTS for part in path.relative_to(repo).parts):
            continue
        if path.is_file():
            files.append(path)

    return files


def find_document_by_terms(
    repo: Path,
    required_terms: list[str],
    any_terms: list[str],
) -> Path | None:
    for path in iter_repo_files(repo):
        lowered = path.relative_to(repo).as_posix().lower()
        if path.suffix.lower() not in DOCUMENT_SUFFIXES:
            continue
        if all(term in lowered for term in required_terms) and any(
            term in lowered for term in any_terms
        ):
            return path

    return None


def find_data_file_by_terms(
    repo: Path,
    required_terms: list[str],
    any_terms: list[str],
) -> Path | None:
    for path in iter_repo_files(repo):
        lowered = path.relative_to(repo).as_posix().lower()
        if path.name == "trugap-evidence.json":
            continue
        if path.suffix.lower() not in DATA_SUFFIXES:
            continue
        if all(term in lowered for term in required_terms) and any(
            term in lowered for term in any_terms
        ):
            return path

    return None
