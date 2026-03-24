from __future__ import annotations

import os
import sys
from pathlib import Path

DB_FILENAME = ".pdf-organizer.db"


def get_workspace_root() -> Path:
    override = os.environ.get("PDF_ORGANIZER_WORKSPACE_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path.cwd().resolve()


def database_path(root: Path | None = None) -> Path:
    return (root or get_workspace_root()) / DB_FILENAME


def normalize_workspace_pdf_path(path: str | Path, root: Path | None = None) -> Path:
    workspace_root = (root or get_workspace_root()).resolve()
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = workspace_root / candidate
    resolved = candidate.resolve()
    if resolved.suffix.lower() != ".pdf":
        raise ValueError("Selected file must be a PDF.")
    try:
        relative = resolved.relative_to(workspace_root)
    except ValueError as exc:
        raise ValueError("Selected file must be inside the workspace directory.") from exc
    return relative


def resolve_workspace_pdf_path(relative_path: str | Path, root: Path | None = None) -> Path:
    workspace_root = (root or get_workspace_root()).resolve()
    return (workspace_root / Path(relative_path)).resolve()

