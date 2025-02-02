"""Test of general commands."""

import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pytest

from knx_ga_exporter.argparse import OUTPUT_ENCODING_DEFAULT
from tests.util_runner import run_cli


# ---- Utilities -------------------------------------------------------------------------------------------------------
@dataclass
class ExpectedEvent:
    """Expectation of an event and it's data (summary, description, location, ...)."""

    summary: str
    description: Optional[str]
    location: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]

    def __init__(
        self,
        summary: str,
        description: Optional[str] = None,
        location: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> None:
        """Construct.

        Arguments:
            summary: Event summary
            description: Event description
            location: Event location
            start_date: Start date
            end_date: End date
        """
        self.summary = summary
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date


def read_file(path: str, encoding: str) -> str:
    """Read contents of a local file.

    Arguments:
        path: Path to file
        encoding: File encoding

    Returns:
        Contents of the file.
    """
    local_file = open(path, encoding=encoding)
    return local_file.read()


# ---- Testcases -------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "input_file_path,output_encoding,extra_cli_args,expected_csv_path,expected_logs",
    [
        (
            "tests/inputs/KNX-planning-example.xlsx",
            OUTPUT_ENCODING_DEFAULT,
            "--output.format 1/1 -v",
            "tests/expected_outputs/KNX-planning-example_format_1_1.csv",
            ".*Loading XLSX input file.*KNX-planning-example.xlsx",
        ),
        (
            "tests/inputs/KNX-planning-example.xlsx",
            OUTPUT_ENCODING_DEFAULT,
            "--output.format 3/3 -vv",
            "tests/expected_outputs/KNX-planning-example_format_3_3.csv",
            ".*Parsed GA.*1/2/1.*Top Floor Bedroom.*",
        ),
        (
            "tests/inputs/KNX-planning-example.xlsx",
            OUTPUT_ENCODING_DEFAULT,
            "--output.separator semicolon",
            "tests/expected_outputs/KNX-planning-example_format_1_1_separator_semicolon.csv",
            "INFO.*format: 1/1.*separator: ';'",
        ),
        (
            "tests/inputs/KNX-planning-example.xlsx",
            OUTPUT_ENCODING_DEFAULT,
            "--output.separator comma",
            "tests/expected_outputs/KNX-planning-example_format_1_1_separator_comma.csv",
            "INFO.*format: 1/1.*separator: ','",
        ),
        (
            "tests/inputs/custom-layout.xlsx",
            OUTPUT_ENCODING_DEFAULT,
            "--config tests/inputs/custom-layout-config.json",
            "tests/expected_outputs/custom-layout.csv",
            ".*",
        ),
    ],
)
def test_ct_valid_conversion(
    input_file_path: str,
    output_encoding: str,
    extra_cli_args: str,
    expected_csv_path: str,
    expected_logs: str,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    tmp_path: str,
) -> None:
    """Test valid conversions.

    Arguments:
        input_file_path: CLI arguments
        output_encoding: Output file encoding
        extra_cli_args: Additional CLI arguments
        expected_csv_path: Expected conversion result
        expected_logs: Expected log outputs
        capsys: System capture
        caplog: Logging capture
        tmp_path: Temporary unique file path provided by built-in fixture.
    """
    output_csv_path = f"{tmp_path}/conversion_result.csv"

    cli_args = (
        f"--input.file {input_file_path} --output.file {output_csv_path} --output.encoding {output_encoding} "
        + f"{extra_cli_args}"
    )
    with caplog.at_level(logging.DEBUG):
        cli_result = run_cli(cli_args, capsys)
        assert cli_result.exit_code == os.EX_OK

    output_csv = read_file(output_csv_path, output_encoding)
    expected_csv = read_file(expected_csv_path, output_encoding)
    assert output_csv == expected_csv
    assert re.search(expected_logs, caplog.text)


@pytest.mark.parametrize(
    "input_file_path,expected_error",
    [
        (
            "tests/inputs/missing-maingroup-name.xlsx",
            r"Incomplete KNX group address detected.*1/0/0.*Missing main group name",
        ),
        (
            "tests/inputs/encoding-error.xlsx",
            r"Encoding Error of „long“ minus character",
        ),
    ],
)
def test_ct_invalid_conversion(
    input_file_path: str,
    expected_error: str,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
    tmp_path: str,
) -> None:
    """Test invalid conversions. Expected to fail.

    Arguments:
        input_file_path: CLI arguments
        expected_error: Expected error message
        capsys: System capture
        caplog: Logging capture
        tmp_path: Temporary unique file path provided by built-in fixture.
    """
    output_csv_path = f"{tmp_path}/conversion_result.csv"

    cli_args = f"--input.file {input_file_path} --output.file {output_csv_path} "

    with caplog.at_level(logging.ERROR):
        cli_result = run_cli(cli_args, capsys)
        assert cli_result.exit_code != os.EX_OK

    assert re.search(expected_error, caplog.text)

    # output_csv = read_file(output_csv_path, output_encoding)
    # expected_csv = read_file(expected_csv_path, output_encoding)
    # assert output_csv == expected_csv
