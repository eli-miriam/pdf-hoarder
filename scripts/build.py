from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if shutil.which("pyinstaller") is None:
        print("PyInstaller is not installed. Install the build extra first:", file=sys.stderr)
        print("  pip install .[build]", file=sys.stderr)
        return 1
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name",
        "pdf-organizer",
        "--windowed",
        "--paths",
        str(ROOT / "src"),
        str(ROOT / "src" / "pdf_organizer" / "__main__.py"),
    ]
    return subprocess.call(command, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())

