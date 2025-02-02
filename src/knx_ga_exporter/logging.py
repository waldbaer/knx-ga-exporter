"""Handling of different output target and formats."""

# ---- Imports ---------------------------------------------------------------------------------------------------------
import logging

# ---- Functions -------------------------------------------------------------------------------------------------------


def configure_logging(verbosity_level: int) -> None:
    """Config logging infrastructure.

    Arguments:
        verbosity_level: Configured verbosity level
    """
    log_level = logging.WARN
    if verbosity_level == 1:
        log_level = logging.INFO
    elif verbosity_level >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
