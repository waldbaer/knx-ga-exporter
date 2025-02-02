"""Argument parsing."""

# ---- Imports ----
from typing import Optional

from jsonargparse import ArgumentParser, DefaultHelpFormatter
from rich_argparse import RawTextRichHelpFormatter

from .exporter import CsvFormat, CsvSeparator

# ---- Globals ---------------------------------------------------------------------------------------------------------

OUTPUT_ENCODING_DEFAULT = "iso-8859-1"


# ---- CommandLine parser ----------------------------------------------------------------------------------------------
class HelpFormatter(DefaultHelpFormatter, RawTextRichHelpFormatter):
    """Custom CLI help formatter: Combined DefaultHelpFormatter and RichHelpFormatter."""


def parse_config(prog: str, version: str, copy_right: str, author: str, arg_list: Optional[list[str]] = None) -> dict:
    """Parse the configuration from CLI and/or configuration JSON file.

    Arguments:
        prog: Program name.
        version: Program version.
        copy_right: Copyright info.
        author: Author info.
        arg_list: Optional command line arguments list.

    Returns:
        Dict: Parsed configuration options.
    """
    arg_parser = ArgumentParser(
        prog=prog,
        description="Converter for spreadsheets to KNX ETS group address configurations in CSV format."
        + f" | Version {version} | {copy_right}",
        version=f"| Version {version}\n{copy_right} {author}",
        default_config_files=["./config.json"],
        print_config=None,
        env_prefix="KNX_GA_EXPORTER",
        default_env=False,
        formatter_class=HelpFormatter,
    )

    arg_parser.add_argument("-c", "--config", action="config", help="""Path to JSON configuration file.""")
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase log-level. -v: INFO, -vv DEBUG. Default: WARN/ERROR",
    )

    # ---- Input / Output ----
    arg_parser.add_argument("-i", "--input.file", required=True, help="Path to XSLX file to be parsed.")
    arg_parser.add_argument(
        "-o",
        "--output.file",
        required=False,
        default="knx-ga-addresses.csv",
        help="Path of exported CSV file.",
    )
    arg_parser.add_argument(
        "--output.encoding",
        required=False,
        default=OUTPUT_ENCODING_DEFAULT,
        help="Output file encoding",
    )

    arg_parser.add_argument(
        "--output.format",
        default=str(CsvFormat.format_1_1),
        choices=[str(CsvFormat.format_1_1), str(CsvFormat.format_3_3)],
        help="""CSV output format.

Possible formats:
1/1: Name / Address
3/3: Main- Middle- Sub- Name/Main- Middle- Sub-Address
""",
    )
    arg_parser.add_argument(
        "--output.separator",
        default=CsvSeparator.tabulator,
        type=CsvSeparator,
        help="""CSV separator.

Possible separators:
tabulator: [TAB]
comma:     ,
semicolon: ;
""",
    )

    # ---- Sheet Config ----
    arg_parser.add_argument(
        "--layout.sheet-name",
        default="KNX Group Addresses",
        help="Name of XLSX sheet containing the KNX group addresses",
    )
    arg_parser.add_argument("--layout.first-row", default=8, help="First row containing GAs")
    arg_parser.add_argument("--layout.last-column", default=10, help="Last column")

    arg_parser.add_argument("--layout.main-ID-column", default=0, help="Column containing main ID of KNX GA")
    arg_parser.add_argument("--layout.middle-ID-column", default=2, help="Column containing middle ID of KNX GA")
    arg_parser.add_argument("--layout.sub-ID-column", default=4, help="Column containing sub ID of KNX GA")

    arg_parser.add_argument("--layout.main-name-column", default=1, help="Column containing main name of KNX GA")
    arg_parser.add_argument("--layout.middle-name-column", default=3, help="Column containing middle name of KNX GA")
    arg_parser.add_argument("--layout.sub-name-column", default=8, help="Column containing sub name of KNX GA")

    arg_parser.add_argument("--layout.dpt-column", default=5, help="Column containing datapoint type of KNX GA")
    arg_parser.add_argument("--layout.target-ID-column", default=6, help="Column containing target ID KNX GA")
    arg_parser.add_argument("--layout.comment-column", default=9, help="Column containing GA comment")

    # ---- Finally parse the inputs  ----
    config = arg_parser.parse_args(args=arg_list)

    return config
