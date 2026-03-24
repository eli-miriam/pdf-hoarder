# pdf-tagging-and-search Specification

## Purpose
TBD - created by archiving change build-local-pdf-organizer. Update Purpose after archive.
## Requirements
### Requirement: Global tag catalog management
The system SHALL maintain a global list of tags that users can create and delete from the GUI.

#### Scenario: Add tag to global list
- **WHEN** the user creates a new tag from the tag-management interface
- **THEN** the system adds that tag to the global tag list

#### Scenario: Remove tag from global list
- **WHEN** the user deletes a tag from the global tag list
- **THEN** the system removes the tag from the catalog and removes its assignments from PDF records

### Requirement: Record-level tag assignment
The system SHALL allow users to add and remove tags on each PDF record independently of other record metadata.

#### Scenario: Assign existing tag to record
- **WHEN** the user adds a tag from the global tag list to a PDF record
- **THEN** the system associates that tag with the selected record

#### Scenario: Remove tag from record
- **WHEN** the user removes a tag from a PDF record
- **THEN** the system deletes only that record-tag association

### Requirement: Editable descriptive metadata
The system SHALL allow users to edit record metadata fields, including title and description, after a PDF record is created.

#### Scenario: Update record description
- **WHEN** the user saves changes to a PDF record's description
- **THEN** the system persists the updated description for later viewing and search

### Requirement: Metadata search
The system SHALL provide search over registered PDF records using stored metadata, including title, description, and tags.

#### Scenario: Find record by title text
- **WHEN** the user searches for text that matches a record title
- **THEN** the system includes that record in the search results

#### Scenario: Find record by tag
- **WHEN** the user filters or searches using a tag assigned to one or more records
- **THEN** the system returns the records associated with that tag

