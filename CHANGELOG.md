# Changelog

All notable changes to this project will be documented in this file.

## [2.0.2] - 2025-07-31

### Fixes
- Ignore also empty combinations of sub-name / target ID

### Dependencies
- Bump jsonargparse from 4.38.0 to 4.40.0
- Bump rich-argparse from 1.7.0 to 1.7.1 (#8)


## [2.0.1] - 2025-04-02

### Dependencies
- Bump jsonargparse from 4.36.0 to 4.38.0
- Bump rich-argparse from 1.6.0 to 1.7.0


## [2.0.0] - 2025-02-02

### Features
- Support configuration via JSON (based on [jsonargparse](https://jsonargparse.readthedocs.io/))

### Infrastructure
- Rework to [hyper-modern structure](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) with [python-pdm](https://pdm-project.org/)
- Implement tests (100% coverage)
- Publish to [PyPI](https://pypi.org/) index

### Dependencies
- Bump openpyxl to 3.1.5


## [1.0.1] - 2022-10-28

### Fixes & Improvements

- Detect missing group address (GA).
- Handling of encoding errors.
- Improved log output formatting.

## [1.0.0] - 2021-03-10

Initial Release
