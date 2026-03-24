## Context

The tool is a local desktop application that lives inside the same directory tree as the PDFs it manages. It must run on Linux and Windows, present a GUI, keep PDF files in place, and remain functional when the entire managed directory is copied or moved elsewhere on disk. The application therefore needs a persistence model that is portable across directory moves, a file-selection flow constrained to the managed workspace, and a packaging approach that produces a standalone executable for both target platforms.

## Goals / Non-Goals

**Goals:**
- Provide a desktop GUI for browsing registered PDFs, editing metadata, managing tags, and searching records.
- Persist PDF records in a local database without storing PDF binary contents.
- Store file references relative to the application directory so the workspace remains portable.
- Detect and surface missing-file conditions when a registered PDF is no longer present.
- Produce distributable executables for Linux and Windows from one codebase.

**Non-Goals:**
- Managing PDFs outside the application's own directory tree.
- Syncing records across devices or to a remote service.
- Editing PDF contents or extracting full-text search from PDF bodies in the first iteration.
- Watching the filesystem for external changes in real time.

## Decisions

### Desktop architecture
Use a cross-platform desktop shell with a local web-based UI and bundled backend logic, such as Tauri or Electron, so one codebase can serve both Linux and Windows executables. This fits the requirement for a GUI plus native filesystem access. A purely native toolkit would increase platform-specific implementation overhead, while a browser-only app would not package cleanly as a local executable.

### Workspace root and path model
Treat the executable's parent directory as the workspace root. Every registered PDF path must be validated to ensure it resolves under that root, then stored as a normalized relative path from the root. This keeps links portable when the whole workspace moves and prevents the database from pointing at out-of-scope files elsewhere on disk. Absolute paths were rejected because they would break after copying the directory.

### Persistence model
Use a local embedded database stored beside the executable, with normalized tables for PDF records, tags, and record-tag assignments. Each PDF record stores a stable identifier, title, description, relative file path, created/updated timestamps, and a status derived from file resolution. SQLite is the likely fit because it is portable, embedded, and available on Linux and Windows without running a separate service. Storing metadata in ad hoc JSON files was rejected because relational tag queries and integrity checks would become harder as the dataset grows.

### Record lifecycle
Creating a record starts with a directory-browse flow scoped to the workspace root. When a PDF is selected, the application creates a database row, seeds the title from the filename stem, and leaves the original file untouched. Deleting a record removes only database state and tag associations. Record views resolve the relative path back to a file on disk each time, exposing an explicit missing-file error if resolution fails or the file no longer exists.

### Search and tagging
Search operates on database metadata fields rather than PDF contents. Tags are managed as a reusable global list, with record-tag associations supporting add and remove operations independently from tag-list maintenance. This keeps the first release focused on structured organization and avoids the complexity of OCR or document indexing.

### Packaging
Build release artifacts per platform that bundle the UI, backend logic, and embedded database support into a standalone executable. The executable expects its database file to reside in the same workspace directory, creating it on first run if absent. Packaging must avoid hard-coded install paths so the application remains relocatable.

## Risks / Trade-offs

- [Users move or rename PDFs outside the app] -> Resolve file existence on each record view and search result interaction, and show a clear missing-file status instead of assuming the stored path is valid.
- [Relative-path validation differs between Linux and Windows path semantics] -> Centralize path normalization and workspace-boundary checks in one filesystem service with cross-platform tests.
- [Desktop-shell choice affects executable size and developer ergonomics] -> Choose the shell after a small spike focused on filesystem access, packaging, and startup behavior rather than on UI preference alone.
- [Search expectations may expand to full-text PDF search] -> Keep metadata search as an explicit first-scope limit in specs and tasks so later document indexing can be added as a separate change.

## Migration Plan

There is no existing system to migrate. Initial rollout creates the embedded database in the workspace directory on first launch and supports importing records only through the GUI's link-file flow. Rollback consists of removing the executable and local database file; PDF files on disk remain unchanged because the tool never stores or mutates PDF contents.

## Open Questions

- Which desktop shell should be selected after the implementation spike: Tauri for smaller binaries or Electron for broader plugin familiarity?
- Should the GUI offer a direct "open containing folder" action, a direct "open file" action, or both?
- Should missing-file records remain searchable by default, or appear only when an explicit filter is enabled?
