"""Test of general commands."""

import importlib
import logging
import os
import re

import pytest

from knx_ga_exporter.__main__ import __dist_name__, __prog__
from tests.util_runner import run_cli

# ---- Testcases -------------------------------------------------------------------------------------------------------


def test_ct_help(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the --help option.

    Arguments:
        capsys: System capture
    """
    args = "--help"

    cli_result = run_cli(args, capsys)

    assert cli_result.exit_code == os.EX_OK
    assert cli_result.stdout.startswith(f"Usage: {__prog__}")


def test_ct_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the --version option.

    Arguments:
        capsys: System capture
    """
    args = "--version"

    cli_result = run_cli(args, capsys)

    assert cli_result.exit_code == os.EX_OK
    assert importlib.metadata.version(__dist_name__) in cli_result.stdout
    assert importlib.metadata.version(__prog__) in cli_result.stdout


@pytest.mark.parametrize(
    "cli_args,expected_output",
    [
        (
            "",
            r"input.*is required but not included",
        ),
        (
            "--input.file PATH_TO_UNKNOWN_FILE.XLSX",
            r"No such file or directory.*PATH_TO_UNKNOWN_FILE.XLSX",
        ),
        (
            "--output.format 3/x",
            r"invalid.*3/x",
        ),
    ],
)
def test_ct_invalid_arguments(
    cli_args: str,
    expected_output: str,
    capsys: pytest.CaptureFixture[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that invalid cli arguments are detected.

    Arguments:
        cli_args: Tested command line arguments
        expected_output: Expected output (RegEx)
        capsys: System capture
        caplog: Logging capture
    """
    with caplog.at_level(logging.DEBUG):
        cli_result = run_cli(cli_args, capsys)
        assert cli_result.exit_code != os.EX_OK

    assert re.search(expected_output, cli_result.stderr) or re.search(expected_output, caplog.text)
