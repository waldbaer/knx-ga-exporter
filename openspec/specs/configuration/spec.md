# configuration Specification

## Purpose

Defines how users supply options, through command-line flags and JSON configuration files, and how those sources combine, so spreadsheet layouts and output settings can be stored and reused.

## Requirements

### Requirement: Option naming
Options SHALL be grouped into the namespaces `input`, `output` and `layout`, plus the top-level options `config` and `verbose`. On the command line an option SHALL be written as `--<namespace>.<name>` with dashes. In a JSON configuration file the same option SHALL be a nested key with underscores. Key names are case-sensitive.

#### Scenario: Same option on the command line and in JSON
- **WHEN** a JSON configuration file contains `{"layout": {"sheet_name": "KNX GAs"}}`
- **THEN** the effect is the same as passing `--layout.sheet-name "KNX GAs"`

#### Scenario: Mixed-case key
- **WHEN** a JSON configuration file sets the main-ID column
- **THEN** the key is written as `main_ID_column`, matching the command-line flag `--layout.main-ID-column`

### Requirement: Explicit configuration file
`-c` / `--config <path>` SHALL load option values from the given JSON file. Any option, including `input.file`, MAY be set in the file.

#### Scenario: Custom layout from a configuration file
- **WHEN** the user runs `knx-ga-exporter --config custom-layout-config.json -i custom-layout.xlsx`
- **THEN** the worksheet name, first row and column positions from the file are used

#### Scenario: All options from a configuration file
- **WHEN** a configuration file sets `input.file`, `output.file`, `output.format`, `output.separator` and the layout
- **AND** the user runs `knx-ga-exporter -c <that file>` with no other options
- **THEN** the conversion uses only the values from the file and exits with code 0

### Requirement: Default configuration file
If a file named `config.json` exists in the current working directory, it SHALL be loaded automatically before any command-line option is applied. If it does not exist, the built-in defaults SHALL be used without a warning or error.

#### Scenario: Default configuration file present
- **WHEN** `./config.json` exists and the user runs the command without `--config`
- **THEN** the option values from `./config.json` are used

#### Scenario: Default configuration file absent
- **WHEN** `./config.json` does not exist
- **THEN** the built-in defaults are used and the conversion proceeds normally

### Requirement: Precedence of option sources
Option values SHALL be resolved from lowest to highest priority as: built-in defaults, `./config.json`, then command-line arguments processed from left to right. A file loaded with `--config` SHALL override values given before it and be overridden by values given after it.

#### Scenario: Command-line value after --config wins
- **WHEN** the user runs `--config custom-layout-config.json --layout.sheet-name Other`
- **THEN** the worksheet `Other` is used

#### Scenario: Command-line value before --config loses
- **WHEN** the user runs `--layout.sheet-name Other --config custom-layout-config.json`
- **THEN** the worksheet name from `custom-layout-config.json` is used

#### Scenario: Explicit configuration file overrides the default file
- **WHEN** `./config.json` sets a worksheet name and the user also passes `--config custom-layout-config.json`
- **THEN** the worksheet name from `custom-layout-config.json` is used

### Requirement: Environment variables are ignored
The tool SHALL NOT read option values from environment variables.

#### Scenario: Environment variable set
- **WHEN** an environment variable such as `KNX_GA_EXPORTER_OUTPUT__FORMAT=3/3` is set
- **THEN** the output format is still taken from the defaults, configuration files and command line only
