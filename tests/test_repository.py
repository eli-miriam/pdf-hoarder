from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from src.pdf_organizer.db import connect
from src.pdf_organizer.repository import PdfRepository
from src.pdf_organizer.workspace import normalize_workspace_pdf_path, resolve_workspace_pdf_path


class RepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temp_dir.name)
        os.environ["PDF_ORGANIZER_WORKSPACE_ROOT"] = str(self.workspace)
        self.connection = connect(self.workspace)
        self.repository = PdfRepository(self.connection, self.workspace)
        self.pdf_path = self.workspace / "docs" / "Quarterly Report.pdf"
        self.pdf_path.parent.mkdir(parents=True, exist_ok=True)
        self.pdf_path.write_bytes(b"%PDF-1.4\n")

    def tearDown(self) -> None:
        self.connection.close()
        os.environ.pop("PDF_ORGANIZER_WORKSPACE_ROOT", None)
        self.temp_dir.cleanup()

    def test_normalize_path_requires_workspace_member(self) -> None:
        outside = Path(self.temp_dir.name).parent / "other.pdf"
        outside.write_bytes(b"%PDF-1.4\n")
        with self.assertRaises(ValueError):
            normalize_workspace_pdf_path(outside, self.workspace)
        outside.unlink()

    def test_relative_paths_survive_workspace_copy(self) -> None:
        record = self.repository.add_pdf(self.pdf_path)
        copied_workspace = self.workspace.parent / f"{self.workspace.name}-copy"
        copied_workspace.mkdir()
        copied_pdf = copied_workspace / record.relative_path
        copied_pdf.parent.mkdir(parents=True, exist_ok=True)
        copied_pdf.write_bytes(b"%PDF-1.4\n")
        resolved = resolve_workspace_pdf_path(record.relative_path, copied_workspace)
        self.assertEqual(resolved, copied_pdf.resolve())

    def test_missing_file_detection(self) -> None:
        record = self.repository.add_pdf(self.pdf_path)
        self.pdf_path.unlink()
        updated = self.repository.get_record(record.id)
        self.assertFalse(updated.file_exists)
        self.assertEqual(updated.status, "Missing")

    def test_delete_record_keeps_file(self) -> None:
        record = self.repository.add_pdf(self.pdf_path)
        self.repository.delete_record(record.id)
        self.assertTrue(self.pdf_path.exists())
        self.assertEqual(self.repository.list_records(), [])

    def test_tag_catalog_and_assignment(self) -> None:
        record = self.repository.add_pdf(self.pdf_path)
        self.repository.create_tag("finance")
        self.repository.create_tag("urgent")
        updated = self.repository.set_record_tags(record.id, ["finance", "urgent"])
        self.assertEqual(updated.tags, ["finance", "urgent"])
        self.repository.delete_tag("finance")
        refreshed = self.repository.get_record(record.id)
        self.assertEqual(refreshed.tags, ["urgent"])

    def test_metadata_search(self) -> None:
        record = self.repository.add_pdf(self.pdf_path)
        self.repository.update_record(record.id, "Quarterly Report", "board package")
        self.repository.create_tag("finance")
        self.repository.set_record_tags(record.id, ["finance"])
        self.assertEqual(len(self.repository.list_records("quarterly")), 1)
        self.assertEqual(len(self.repository.list_records("board")), 1)
        self.assertEqual(len(self.repository.list_records("finance")), 1)


if __name__ == "__main__":
    unittest.main()
