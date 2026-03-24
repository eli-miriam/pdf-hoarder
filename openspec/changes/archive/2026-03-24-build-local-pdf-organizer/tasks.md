## 1. Project setup and architecture spike

- [x] 1.1 Select and scaffold the cross-platform desktop shell for Linux and Windows packaging
- [x] 1.2 Establish the application workspace model so the executable directory is treated as the managed root
- [x] 1.3 Add the local persistence dependency and create the initial database bootstrap flow

## 2. Persistence and filesystem services

- [x] 2.1 Implement the database schema for PDF records, tags, and record-tag assignments
- [x] 2.2 Implement path normalization and workspace-boundary validation for Linux and Windows filesystem semantics
- [x] 2.3 Store linked PDF locations as workspace-relative paths and resolve them back to disk paths at runtime
- [x] 2.4 Implement missing-file detection and record status reporting when a linked PDF cannot be found

## 3. PDF record management flows

- [x] 3.1 Implement the GUI flow to browse the workspace and register a PDF without copying file contents
- [x] 3.2 Seed new record titles from the selected PDF filename and persist editable title and description fields
- [x] 3.3 Implement record detail views that show metadata, linked path, and current file status
- [x] 3.4 Implement record deletion that removes only application data and leaves the PDF on disk untouched

## 4. Tagging and search

- [x] 4.1 Implement global tag creation and deletion in the GUI and persistence layer
- [x] 4.2 Implement adding and removing tag assignments on individual PDF records
- [x] 4.3 Implement metadata search across title, description, and tags
- [x] 4.4 Decide and implement the UI behavior for whether missing-file records appear in default search results

## 5. Desktop actions, packaging, and verification

- [x] 5.1 Implement the record action that opens the linked file or containing location through the host operating system
- [x] 5.2 Configure reproducible Linux and Windows executable packaging without hard-coded install paths
- [x] 5.3 Add tests for workspace scoping, relative-path portability, missing-file handling, and record-only deletion
- [x] 5.4 Add tests for tag catalog management, record tag assignment, and metadata search behavior
