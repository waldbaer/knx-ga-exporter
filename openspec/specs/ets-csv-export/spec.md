# ets-csv-export Specification

## Purpose

Defines the CSV file produced for the KNX ETS group address import (Edit → Import Group Addresses): the 1/1 and 3/3 layouts, the group hierarchy, separators, quoting, encoding, and how names and descriptions are built.

## Requirements

### Requirement: Output file
The CSV SHALL be written to `output.file` (default `knx-ga-addresses.csv`, relative to the current working directory). An existing file at that path SHALL be overwritten.

#### Scenario: Default output path
- **WHEN** no output file is configured
- **THEN** the CSV is written to `./knx-ga-addresses.csv`

#### Scenario: Existing file
- **WHEN** the output file already exists
- **THEN** its previous content is replaced by the new export

### Requirement: Output format selection
`output.format` SHALL select the CSV layout: `1/1` (default; one name column and one address column) or `3/3` (separate name and address columns for main, middle and sub group). Any other value MUST be rejected as a usage error.

#### Scenario: Default format
- **WHEN** no format is configured
- **THEN** the file uses the 1/1 layout

#### Scenario: 3/3 format
- **WHEN** the user passes `--output.format 3/3`
- **THEN** the file uses the 3/3 layout

### Requirement: Group hierarchy
After the header row, the file SHALL contain one row per main group, followed by one row per middle group in that main group, each followed by its group address rows. Each main and middle group SHALL appear once, named after the first exported group address that belongs to it.

#### Scenario: Hierarchy in the example workbook
- **WHEN** the example workbook is exported in 1/1 format
- **THEN** the first rows after the header are, in order:
  - `"Light & Power"` with address `0/-/-`
  - `"Switch"` with address `0/0/-`
  - the group addresses `0/0/1`, `0/0/2`, `0/0/3` and `0/0/5`
  - `"Status"` with address `0/1/-`

#### Scenario: Conflicting group names
- **WHEN** two rows in middle group 3/5 give the middle group name as `M5` and then `M5-other`
- **THEN** the middle group row is named `M5`

#### Scenario: Order of group addresses
- **WHEN** a middle group contains sub group 9 in an earlier row and sub group 2 in a later row
- **THEN** 3/5/9 is written before 3/5/2, following the spreadsheet row order

#### Scenario: No group addresses
- **WHEN** no row in the worksheet yields a group address
- **THEN** the file contains only the header row

### Requirement: 1/1 format columns
In 1/1 format the header SHALL be `Group name`, `Address`, `Central`, `Unfiltered`, `Description`, `DatapointType`, `Security`. Addresses SHALL be written as `<main>/-/-` for main groups, `<main>/<middle>/-` for middle groups and `<main>/<middle>/<sub>` for group addresses.

#### Scenario: 1/1 rows
- **WHEN** main group 0 `Light & Power`, middle group 0 `Switch` and group address 0/0/1 are exported in 1/1 format with `--output.separator semicolon`
- **THEN** the rows are:
  - `"Light & Power";"0/-/-";"";"";"";"";"Auto"`
  - `"Switch";"0/0/-";"";"";"";"";"Auto"`
  - `"B0-0-L - Basement Office - Ceiling light - Light & Power Switch";"0/0/1";"";"";"Additional comment";"DPST-1-1";"Auto"`

### Requirement: 3/3 format columns
In 3/3 format the header SHALL be `Main`, `Middle`, `Sub`, `Main`, `Middle`, `Sub`, `Central`, `Unfiltered`, `Description`, `DatapointType`, `Security`. Each row SHALL put its name in the name column for its level and fill the address columns down to that level, leaving the others empty.

#### Scenario: 3/3 rows
- **WHEN** main group 0 `Light & Power`, middle group 0 `Switch` and group address 0/0/1 are exported in 3/3 format with `--output.separator semicolon`
- **THEN** the rows are:
  - `"Light & Power";"";"";"0";"";"";"";"";"";"";"Auto"`
  - `"";"Switch";"";"0";"0";"";"";"";"";"";"Auto"`
  - `"";"";"B0-0-L - Basement Office - Ceiling light - Light & Power Switch";"0";"0";"1";"";"";"Additional comment";"DPST-1-1";"Auto"`

### Requirement: Fixed ETS column values
In both formats, `Central` and `Unfiltered` SHALL always be empty and `Security` SHALL always be `Auto`. Main and middle group rows SHALL have an empty `Description` and `DatapointType`.

#### Scenario: Group row values
- **WHEN** any main or middle group row is written
- **THEN** its `Central`, `Unfiltered`, `Description` and `DatapointType` fields are empty
- **AND** its `Security` field is `Auto`

#### Scenario: Group address row values
- **WHEN** any group address row is written
- **THEN** its `Central` and `Unfiltered` fields are empty
- **AND** its `DatapointType` field holds the datapoint type from the spreadsheet
- **AND** its `Security` field is `Auto`

### Requirement: Separator
`output.separator` SHALL select the field delimiter: `tabulator` (default, TAB), `comma` (`,`) or `semicolon` (`;`). Any other value MUST be rejected as a usage error.

#### Scenario: Semicolon
- **WHEN** the user passes `--output.separator semicolon`
- **THEN** the header row is `"Group name";"Address";"Central";"Unfiltered";"Description";"DatapointType";"Security"`

#### Scenario: Comma
- **WHEN** the user passes `--output.separator comma`
- **THEN** fields are separated by `,`

#### Scenario: Unsupported separator
- **WHEN** the user passes `--output.separator pipe`
- **THEN** stderr names the allowed values `tabulator`, `comma` and `semicolon`
- **AND** the process exits with code 2

### Requirement: Quoting and line endings
Every field, including empty and numeric fields, SHALL be enclosed in double quotes, and a double quote inside a value SHALL be written as two double quotes. Every row, including the last, SHALL end with CR LF.

#### Scenario: Value containing quotes
- **WHEN** a group address name is `Say "hi"` with target ID `T1`
- **THEN** the field is written as `"T1 - Say ""hi"""`

#### Scenario: Line endings
- **WHEN** any file is exported
- **THEN** each row, including the last, ends with `\r\n`

### Requirement: Output encoding
The file SHALL be written in the character encoding named by `output.encoding` (default `iso-8859-1`). If a value cannot be represented in that encoding, the conversion MUST fail with an error that quotes the affected row and explains that a character cannot be represented, and the process MUST exit with code 1.

#### Scenario: Character not in the default encoding
- **WHEN** an exported name or comment contains a character outside ISO-8859-1, such as `„` or an en dash, and the default encoding is used
- **THEN** an `ERROR` log message starts with `Failed to encode the CSV row string` and quotes the row
- **AND** the process exits with code 1

#### Scenario: UTF-8 output
- **WHEN** the same workbook is exported with `--output.encoding utf-8`
- **THEN** the conversion succeeds and the character is written as UTF-8

### Requirement: Group address name
A group address name SHALL be the name from the spreadsheet. When a target ID is present (not empty and not 0), the name SHALL be `<target ID> - <name>`, with each line break replaced by `_`.

#### Scenario: Name with target ID
- **WHEN** a row has target ID `B0-0-L` and name `Basement Office - Ceiling light - Light & Power Switch`
- **THEN** the exported name is `B0-0-L - Basement Office - Ceiling light - Light & Power Switch`

#### Scenario: Name without target ID
- **WHEN** a row has no target ID and the name `Lamp`
- **THEN** the exported name is `Lamp`

#### Scenario: Multi-line name with target ID
- **WHEN** a row has target ID `T2` and a name with two lines `d` and `line2`
- **THEN** the exported name is `T2 - d_line2`

### Requirement: Group address description
The `Description` field of a group address SHALL contain the comment from the spreadsheet, with each line break replaced by `|`. An empty comment SHALL give an empty description.

#### Scenario: Single-line comment
- **WHEN** a row has the comment `Additional comment`
- **THEN** the `Description` field is `Additional comment`

#### Scenario: Multi-line comment
- **WHEN** a row has a comment with two lines `x` and `y`
- **THEN** the `Description` field is `x|y`

#### Scenario: No comment
- **WHEN** a row has no comment
- **THEN** the `Description` field is empty
