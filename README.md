# PDF Organizer

PDF Organizer is a local desktop application for managing PDF metadata inside a single workspace directory. The application stores records, tags, and search metadata in SQLite while leaving PDF files in place on disk.

## Features

- Register PDFs from the current workspace directory tree
- Store portable relative links so copied workspaces still function
- Edit record title and description
- Manage a global tag catalog and assign tags to records
- Search records by title, description, and tags
- Detect and display missing-file status
- Open the file or containing folder from the GUI
- Delete records without deleting PDF files

## Workspace model

When packaged, the workspace root is the directory that contains the executable. During source development, the workspace root defaults to the current working directory. Set `PDF_ORGANIZER_WORKSPACE_ROOT` to override this for local testing.

The SQLite database is created as `.pdf-organizer.db` inside the workspace root.

## Run from source

```bash
python3 -m src.pdf_organizer
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Packaging

Install the optional build dependency and run:

```bash
python3 scripts/build.py
```

The build script packages the application with PyInstaller so the resulting executable can be placed directly in the PDF workspace directory on Linux or Windows.

