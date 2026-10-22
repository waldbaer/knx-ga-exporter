# cli Specification

## Purpose

Defines how the `knx-ga-exporter` command is invoked, how it reports progress and errors, and which exit codes it returns, so it can be used both interactively and from scripts.

## Requirements

### Requirement: One conversion per invocation
Each run of `knx-ga-exporter` SHALL read one input spreadsheet, extract its group addresses, write one CSV file and then exit. The input file (`-i` / `--input.file`) MUST be provided, either on the command line or in a configuration file.

#### Scenario: Successful conversion
- **WHEN** the user runs `knx-ga-exporter -i KNX-planning-example.xlsx`
- **THEN** the CSV file is written to the configured output path
- **AND** the process exits with code 0

#### Scenario: Input file not given
- **WHEN** the user runs `knx-ga-exporter` with no input file on the command line or in any configuration file
- **THEN** stderr reports that `input.file` is a required argument
- **AND** the process exits with code 2
- **AND** no CSV file is written

### Requirement: Help output
`-h` / `--help` SHALL print a usage summary that lists every option with its description and default value, and the process MUST exit with code 0 without reading any input.

#### Scenario: Show help
- **WHEN** the user runs `knx-ga-exporter --help`
- **THEN** stdout starts with `Usage: knx-ga-exporter`
- **AND** the process exits with code 0

### Requirement: Version output
`--version` SHALL print the program name, the installed package version, the copyright notice and the author, and the process MUST exit with code 0 without reading any input.

#### Scenario: Show version
- **WHEN** the user runs `knx-ga-exporter --version`
- **THEN** stdout contains `knx-ga-exporter | Version <installed version>`
- **AND** the next line contains the copyright notice and author name
- **AND** the process exits with code 0

### Requirement: Log verbosity
Log messages SHALL be written to stderr as `<YYYY-MM-DD HH:MM:SS> <LEVEL>: <message>`. By default only warnings and errors SHALL be shown. `-v` SHALL add informational messages, and `-vv` (or more `v`s) SHALL add debug messages.

#### Scenario: Default verbosity
- **WHEN** a conversion succeeds without `-v`
- **THEN** nothing is written to stdout or stderr

#### Scenario: Informational logging
- **WHEN** a conversion runs with `-v`
- **THEN** the log contains `Loading XLSX input file '<input path>'`
- **AND** the log contains `Exporting group addresses into CSV file '<output path>'. format: <format>, separator: '<separator>', encoding: <encoding>`, with a tab separator shown as `[TAB]`
- **AND** the log ends with `Conversion successfully finished.`

#### Scenario: Debug logging
- **WHEN** a conversion runs with `-vv`
- **THEN** the log additionally contains a `Parsed GA: ...` line for each group address read
- **AND** a line for each main group, middle group and group address written
- **AND** a `Statistics: #GA: <count>` line with the number of group addresses exported

### Requirement: Usage errors
Invalid command-line usage (unknown option, missing required option, or a value outside an option's allowed choices) SHALL print the usage summary and an error message to stderr, and the process MUST exit with code 2.

#### Scenario: Invalid choice
- **WHEN** the user passes `--output.format 3/x`
- **THEN** stderr contains `invalid choice: '3/x'`
- **AND** the process exits with code 2

### Requirement: Conversion errors
Any failure after the options are parsed (for example a missing or unreadable input file, a missing worksheet, an incomplete group address, an encoding error or an unwritable output path) SHALL be logged as a single `ERROR` message, without a stack trace, and the process MUST exit with code 1.

#### Scenario: Input file does not exist
- **WHEN** the user passes `--input.file PATH_TO_UNKNOWN_FILE.XLSX`
- **THEN** an `ERROR` log message contains `No such file or directory` and the path
- **AND** the process exits with code 1

#### Scenario: Output directory does not exist
- **WHEN** the output path points into a directory that does not exist
- **THEN** an `ERROR` log message contains `No such file or directory` and the output path
- **AND** the process exits with code 1
