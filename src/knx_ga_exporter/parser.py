"""Workbook parser."""

# ---- Imports ---------------------------------------------------------------------------------------------------------
import logging

import openpyxl
import openpyxl.workbook

from knx_ga_exporter.group_address import GroupAddress

# ---- Functions -------------------------------------------------------------------------------------------------------


def load_workbook(input_file: str) -> openpyxl.workbook:
    """Load XLX workbook.

    Args:
        input_file (str): Path of input file.

    Returns:
        Loaded workbook
    """
    logging.info("Loading XLSX input file '%s'", input_file)
    wb = openpyxl.load_workbook(filename=input_file, read_only=True, data_only=True)
    return wb


def parse_group_addresses(wb: openpyxl.workbook, config: dict) -> list[GroupAddress]:
    """Parse the group addresses.

    Arguments:
        wb: Workbook
        config: Config hierarchy

    Returns:
        Parsed KNX group addresses
    """
    gas = []
    ws = wb[config.ga_sheet_name]
    for row in ws.iter_rows(min_row=config.ga_sheet_first_row, max_col=config.ga_sheet_last_column):
        target_id = row[config.ga_sheet_target_ID_column].value

        group_main = row[config.ga_sheet_main_ID_column].value
        group_middle = row[config.ga_sheet_middle_ID_column].value
        group_sub = row[config.ga_sheet_sub_ID_column].value

        group_main_name = row[config.ga_sheet_main_name_column].value
        group_middle_name = row[config.ga_sheet_middle_name_column].value
        group_sub_name = row[config.ga_sheet_sub_name_column].value

        dpt = row[config.ga_sheet_dpt_column].value
        compiled_ga = row[config.ga_sheet_compiled_GA_column].value
        comment = row[config.ga_sheet_comment].value

        # Skip invalid / incomplete GAs
        if (dpt is None) or (dpt == 0) or (dpt is None) or (compiled_ga is None) or (compiled_ga == 0):
            continue

        ga = GroupAddress(
            group_main,
            group_middle,
            group_sub,
            group_main_name,
            group_middle_name,
            group_sub_name,
            target_id,
            dpt,
            comment,
        )
        logging.debug("Parsed GA: %s", ga)
        gas.append(ga)

    return gas
