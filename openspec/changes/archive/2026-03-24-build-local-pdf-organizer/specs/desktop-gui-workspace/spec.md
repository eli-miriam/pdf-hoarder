## ADDED Requirements

### Requirement: Local desktop GUI
The system SHALL provide a graphical desktop interface for managing PDF records on both Linux and Windows.

#### Scenario: Launch GUI on supported platform
- **WHEN** the user starts the packaged application on Linux or Windows
- **THEN** the system opens the PDF management GUI without requiring a separate server setup

### Requirement: Directory browsing for linking
The system SHALL provide a GUI flow that lets the user browse the workspace directory tree and select a PDF file to register.

#### Scenario: Browse and select PDF
- **WHEN** the user starts the add-PDF flow from the GUI
- **THEN** the system presents a file-selection experience that allows choosing a PDF inside the workspace

### Requirement: Record detail navigation to file location
The system SHALL provide a record-detail action that navigates the user to the linked file location from the GUI when the file is available.

#### Scenario: Open linked file location
- **WHEN** the user views a PDF record whose file is present on disk and invokes the file-location action
- **THEN** the system opens the linked file or its containing location using the host operating system

### Requirement: Record detail visibility
The system SHALL display each PDF record's core metadata and file status in the GUI.

#### Scenario: View record details
- **WHEN** the user opens a PDF record in the GUI
- **THEN** the system shows the title, description, tags, linked file path, and current file-availability status
