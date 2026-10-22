# spreadsheet-parsing Specification

## Purpose

Defines how KNX group addresses are read from an XLSX workbook: which worksheet, rows and columns are used, which rows are skipped, and which rows stop the conversion as incomplete.

## Requirements

### Requirement: XLSX workbook input
The input file SHALL be an Office Open XML workbook (`.xlsx`). Cell values SHALL be read as last calculated and saved by the spreadsheet application, so a formula cell contributes its saved result, not the formula text. A file that is not a valid workbook MUST stop the conversion with an error.

#### Scenario: Names built by formulas
- **WHEN** the target ID and group address name cells contain formulas that look up values in another worksheet (such as a room book)
- **THEN** the looked-up text saved in the workbook is used as the target ID and name

#### Scenario: Input is not a workbook
- **WHEN** the input file is a plain text file named `something.xlsx`
- **THEN** the conversion fails with an `ERROR` log message and exit code 1

### Requirement: Worksheet selection
Group addresses SHALL be read only from the worksheet named by `layout.sheet_name` (default `KNX Group Addresses`). Other worksheets SHALL be ignored. If no worksheet has that name, the conversion MUST fail with an error that names the missing worksheet.

#### Scenario: Other worksheets present
- **WHEN** the workbook contains the worksheets `KNX Group Addresses` and `Room Book`
- **THEN** only rows from `KNX Group Addresses` are exported

#### Scenario: Worksheet missing
- **WHEN** `layout.sheet_name` is `Nope` and the workbook has no worksheet with that name
- **THEN** an `ERROR` log message contains `Worksheet Nope does not exist.`
- **AND** the process exits with code 1

### Requirement: Row range
Rows SHALL be read from spreadsheet row `layout.first_row` (1-based, default 8) through the last used row of the worksheet. Rows above `layout.first_row`, such as titles and column headings, SHALL be ignored.

#### Scenario: Header rows ignored
- **WHEN** the default layout is used and rows 1 to 7 contain a title and column headings
- **THEN** reading starts at row 8 and rows 1 to 7 produce no group addresses

#### Scenario: No rows at or after the first row
- **WHEN** `layout.first_row` is greater than the number of the last used row
- **THEN** the CSV file contains only its header row
- **AND** the process exits with code 0

### Requirement: Column layout
Only the first `layout.last_column` columns (default 10) SHALL be read. Each field SHALL come from the column given by its `layout.*_column` option, as a 0-based index where 0 is column A. Columns not assigned to a field SHALL be ignored.

#### Scenario: Default column layout
- **WHEN** no layout options are set
- **THEN** the fields are read from these columns:
  - A (`main_ID_column` 0): main group ID
  - B (`main_name_column` 1): main group name
  - C (`middle_ID_column` 2): middle group ID
  - D (`middle_name_column` 3): middle group name
  - E (`sub_ID_column` 4): sub group ID
  - F (`dpt_column` 5): datapoint type
  - G (`target_ID_column` 6): target ID (device or room-book reference)
  - I (`sub_name_column` 8): group address name
  - J (`comment_column` 9): comment
- **AND** column H is ignored

#### Scenario: Custom column layout
- **WHEN** a configuration file sets `sheet_name` to `KNX GAs`, `first_row` to 4 and moves every field to a different column
- **THEN** the same group addresses are extracted as from an equivalent workbook in the default layout

### Requirement: Rows without a datapoint type are skipped
A row SHALL be skipped without any message when its datapoint type cell is empty or 0. This lets the worksheet contain spacer rows, reserved addresses and planned but unused addresses.

#### Scenario: Unused address
- **WHEN** a row has IDs 0/0/4 and the comment `Ignored if no DPT is defined` but no datapoint type
- **THEN** no group address 0/0/4 is exported

#### Scenario: Reserved broadcast address
- **WHEN** a row describes the reserved address 0/0/0 without a datapoint type
- **THEN** it is not exported

### Requirement: Rows without a name are skipped
A row SHALL be skipped without any message when its group address name is empty, 0 or `#N/A` and its target ID is also empty or 0.

#### Scenario: Failed name lookup
- **WHEN** a row has a datapoint type, no target ID, and a name cell whose saved value is `#N/A`
- **THEN** the row is not exported

#### Scenario: Empty name and target
- **WHEN** a row has a datapoint type but both the name and target ID cells are empty
- **THEN** the row is not exported

### Requirement: Incomplete group addresses stop the conversion
Every row that is not skipped MUST have a main group ID, middle group ID, sub group ID, main group name, middle group name, group address name and datapoint type. If any is missing, the conversion SHALL fail with `Incomplete KNX group address detected: <row summary>` and the output file SHALL NOT be created or changed.

#### Scenario: Missing main group name
- **WHEN** a row for group address 1/0/0 has no main group name
- **THEN** an `ERROR` log message matches `Incomplete KNX group address detected.*1/0/0`
- **AND** the process exits with code 1
- **AND** no CSV file is written

#### Scenario: Target ID without a name
- **WHEN** a row has a datapoint type and a target ID but an empty group address name
- **THEN** the conversion fails with `Incomplete KNX group address detected`

### Requirement: Values are exported without KNX validation
Numeric group IDs and datapoint types SHALL be passed to the output exactly as read. The tool SHALL NOT check KNX address ranges (main 0-31, middle 0-7, sub 0-255), datapoint type syntax, or duplicate addresses.

#### Scenario: Out-of-range and duplicate addresses
- **WHEN** two rows both have IDs 40/12/300 and a datapoint type
- **THEN** both are exported with address `40/12/300` and no warning is logged
