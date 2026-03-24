## Why

Managing a growing set of PDFs on disk is awkward when the files need richer metadata than filenames and folders can provide. A local desktop tool is needed to register PDFs in place, attach searchable metadata, and keep the collection portable when the containing directory is moved or copied.

## What Changes

- Add a local desktop application with a GUI for Linux and Windows that manages PDF records for files stored inside the application's working directory tree.
- Allow users to browse the managed directory, link a PDF into the tool's database, and automatically seed the record title from the file's filename.
- Allow users to edit PDF records to maintain metadata such as title, description, and tags without copying PDF contents into the database.
- Support tag management at both the record level and the global tag list level, including adding and removing tags.
- Provide search and filtering across registered PDFs using stored metadata.
- Show file-location actions and missing-file errors when a registered PDF can no longer be found on disk.
- Allow deleting a PDF record without deleting the underlying PDF file.
- Store file references in a portable way so moving or copying the entire managed directory preserves working links.

## Capabilities

### New Capabilities
- `pdf-record-management`: Register PDFs from the managed directory, maintain editable metadata records, and preserve portable file links without copying the source files.
- `pdf-tagging-and-search`: Manage a global tag list, assign and remove tags on records, and search the library using stored metadata.
- `desktop-gui-workspace`: Provide a local GUI workflow for browsing, viewing record details, surfacing missing-file errors, and opening the file location from within the application.

### Modified Capabilities

None.

## Impact

Affected areas include the desktop application shell, the local persistence layer for metadata and tags, file-path handling for portable relative links, and packaging for Linux and Windows executables. The change will also introduce requirements for directory-scoped file discovery, validation of missing files, and GUI flows for record editing and search.
