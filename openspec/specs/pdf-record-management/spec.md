# pdf-record-management Specification

## Purpose
TBD - created by archiving change build-local-pdf-organizer. Update Purpose after archive.
## Requirements
### Requirement: Workspace-scoped PDF registration
The system SHALL allow a user to create a PDF record only for a PDF file located within the application's workspace directory tree, where the workspace root is the executable's parent directory.

#### Scenario: Register PDF inside workspace
- **WHEN** the user browses from the GUI and selects a PDF file whose resolved path is inside the workspace root
- **THEN** the system creates a PDF record linked to that file

#### Scenario: Reject PDF outside workspace
- **WHEN** the user selects a file whose resolved path is outside the workspace root
- **THEN** the system MUST reject the selection and explain that only PDFs inside the managed directory are supported

### Requirement: PDF records preserve files in place
The system SHALL store metadata and a file reference for each registered PDF without copying the PDF binary into the application's database.

#### Scenario: Link file without copying content
- **WHEN** a PDF record is created
- **THEN** the system stores metadata and a file reference only, and leaves the original PDF file unchanged on disk

### Requirement: Record title defaults from filename
The system SHALL initialize a new PDF record's title from the selected PDF's filename, excluding the file extension.

#### Scenario: Seed title from filename
- **WHEN** the user creates a record for `Quarterly Report.pdf`
- **THEN** the new record title is initialized as `Quarterly Report`

### Requirement: Portable file references
The system SHALL store each linked PDF reference in a form that remains valid when the entire workspace directory is moved or copied to another location on disk.

#### Scenario: Resolve record after workspace copy
- **WHEN** the application workspace directory, including the executable, database, and linked PDFs, is copied to a new location
- **THEN** the system resolves existing PDF records successfully in the new location without requiring the user to relink files

### Requirement: Missing files are surfaced
The system SHALL detect when a registered PDF cannot be found at its stored workspace-relative location and SHALL present an explicit missing-file error for that record.

#### Scenario: Record points to missing PDF
- **WHEN** the PDF file for an existing record has been moved, renamed, or deleted outside the application
- **THEN** the system shows the record in an error state indicating that the file cannot be located

### Requirement: Record deletion does not delete files
The system SHALL allow users to delete PDF records without deleting the corresponding PDF files from disk.

#### Scenario: Delete record only
- **WHEN** the user deletes a PDF record
- **THEN** the system removes the database record and leaves the PDF file on disk unchanged

