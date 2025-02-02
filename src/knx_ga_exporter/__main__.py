"""Commandline interface entry point."""

# ---- Imports --------------------------------------------------------------------------------------------------------
import importlib.metadata
import logging
import os
from typing import Optional

from knx_ga_exporter.logging import configure_logging

from .argparse import parse_config
from .exporter import export_csv
from .parser import load_workbook, parse_group_addresses

# ---- Module Meta-Data ------------------------------------------------------------------------------------------------
__prog__ = "knx-ga-exporter"
__dist_name__ = "knx_ga_exporter"
__copyright__ = "Copyright 2019-2025"
__author__ = "Sebastian Waldvogel"

# ---- Main -----------------------------------------------------------------------------------------------------------


def cli(arg_list: Optional[list[str]] = None) -> int:
    """Main command line handling entry point.

    Arguments:
        arg_list: Optional list of command line arguments. Only needed for testing.
                  Productive __main__ will call the API without any argument.

    Returns:
        int: Numeric exit code
    """
    try:
        config = parse_config(
            prog=__prog__,
            version=importlib.metadata.version(__dist_name__),
            copy_right=__copyright__,
            author=__author__,
            arg_list=arg_list,
        )
        return _main_logic(config)

    except SystemExit as e:
        return e.code

    except BaseException as e:  # pylint: disable=broad-exception-caught;reason=Explicitly capture all exceptions thrown during execution.
        logging.error(e)
        return 1


def _main_logic(config: dict) -> int:
    """Main program logic.

    Args:
        config (dict): Config hierarchy

    Returns:
        int: exit code
    """
    configure_logging(config.verbose)
    wb = load_workbook(config.input.file)
    gas = parse_group_addresses(wb, config.layout)
    export_csv(config.output, gas)

    logging.debug("Statistics: #GA: %s", len(gas))
    logging.info("Conversion successfully finished.")

    return os.EX_OK
