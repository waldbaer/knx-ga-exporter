"""Handling of different output target and formats."""

# ---- Imports ---------------------------------------------------------------------------------------------------------
import csv
import logging
from enum import Enum

from knx_ga_exporter.group_address import GroupAddress

# ---- Functions -------------------------------------------------------------------------------------------------------


class CsvFormat(Enum):
    """CSV format types."""

    # Name / Address
    format_3_3 = "3/3"  # pylint: disable=invalid-name;reason=camel_case style wanted for cli param
    # Main- Middle- Sub- Name/Main- Middle- Sub-Address
    format_1_1 = "1/1"  # pylint: disable=invalid-name;reason=camel_case style wanted for cli param

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: String representation
        """
        return self.value


class CsvSeparator(Enum):
    """CSV separator types."""

    tabulator = "tabulator"  # pylint: disable=invalid-name;reason=camel_case style wanted for cli param
    comma = "comma"  # pylint: disable=invalid-name;reason=camel_case style wanted for cli param
    semicolon = "semicolon"  # pylint: disable=invalid-name;reason=camel_case style wanted for cli param

    def __str__(self) -> str:
        """String representation.

        Returns:
            str: String representation
        """
        return self.value


class CsvWriter:
    """Write for CSV files."""

    def __init__(self, file: str, delimiter: str, quoting: str) -> None:
        """Initialize the writer.

        Arguments:
            file: File path
            delimiter: File delimiter
            quoting: File quoting
        """
        self.writer = csv.writer(file, delimiter=delimiter, quoting=quoting)

    def write_row(self, row: str) -> None:
        """Write a single row to the CSV file.

        Arguments:
            row: Row contents

        Raises:
            ValueError: If writing failed due to an encoding error.
        """
        try:
            self.writer.writerow(row)
        except UnicodeEncodeError as e:
            raise ValueError(
                f"""Failed to encode the CSV row string: {row}
Some characters can most-likely not be represented in the selected encoding.
Please use only use characters supported by the encoding.
CSV writer error details: {e}"""
            ) from e


def export_csv(output_config: dict, group_addresses: list[GroupAddress]) -> None:
    """Export KNX group address to CSV.

    Arguments:
        output_config: Output configuration hierarchy.
        group_addresses: KNX group addresses
    """
    csv_separators = {"tabulator": "\t", "comma": ",", "semicolon": ";"}
    exporter_functions = {"1/1": _export_csv_format_1_1, "3/3": _export_csv_format_3_3}

    csv_separator = csv_separators[str(output_config.separator)]

    logging.info(
        "Exporting group addresses into CSV file '%s'. format: %s, separator: '%s', encoding: %s",
        output_config.file,
        output_config.format,
        csv_separator.replace("\t", "[TAB]"),
        output_config.encoding,
    )

    export_function = exporter_functions[str(output_config.format)]
    export_function(output_config.file, output_config.encoding, csv_separator, group_addresses)


def _filter_by_main_id(group_addresses: list[GroupAddress], main_id: int) -> list[GroupAddress]:
    """_Filter list of KNX group addresses by main ID.

    Args:
        group_addresses (list[GroupAddress]): KNX group addresses
        main_id (int): main ID

    Returns:
        list[GroupAddress]: Filtered list
    """
    return list(filter(lambda ga: ga.main == main_id, group_addresses))


def _filter_by_middle_id(group_addresses: list[GroupAddress], middle_id: int) -> list[GroupAddress]:
    """_Filter list of KNX group addresses by middle ID.

    Args:
        group_addresses (list[GroupAddress]): KNX group addresses
        middle_id (int): middle ID

    Returns:
        list[GroupAddress]: Filtered list
    """
    return list(filter(lambda ga: ga.middle == middle_id, group_addresses))


def _export_csv_format_1_1(
    output_file: str, output_file_encoding: str, csv_separator: str, group_addresses: list[GroupAddress]
) -> None:
    """Export KNX group address to CSV in format 'format_1_1'.

    Arguments:
        output_file: Path of output file
        output_file_encoding: Output file encoding
        csv_separator: CSV separator
        group_addresses: KNX group addresses
    """
    with open(output_file, "w", newline="", encoding=output_file_encoding) as csv_file:
        writer = CsvWriter(csv_file, csv_separator, csv.QUOTE_ALL)

        # write headline
        writer.write_row(["Group name", "Address", "Central", "Unfiltered", "Description", "DatapointType", "Security"])

        main_group_ids = {ga.main for ga in group_addresses}
        for main_group_id in main_group_ids:
            filtered_main_gas = _filter_by_main_id(group_addresses, main_group_id)
            main_group_name = filtered_main_gas[0].main_name

            logging.debug(str(f"Exporting main group     {main_group_id:<8d} | {main_group_name} |"))
            writer.write_row([main_group_name, f"{main_group_id}/-/-"] + [""] * 4 + ["Auto"])

            middle_group_ids = {ga.middle for ga in filtered_main_gas}
            for middle_group_id in middle_group_ids:
                filtered_middle_gas = _filter_by_middle_id(filtered_main_gas, middle_group_id)
                middle_group_name = filtered_middle_gas[0].middle_name

                main_middle_ga_formatted = f"{main_group_id}/{middle_group_id}"
                logging.debug(
                    str(
                        "Exporting   middle group "
                        + f"{main_middle_ga_formatted:<8s} | {' ' * len(main_group_name)} | {middle_group_name} |"
                    )
                )
                writer.write_row([middle_group_name, f"{main_group_id}/{middle_group_id}/-"] + [""] * 4 + ["Auto"])

                for sub_ga in filtered_middle_gas:
                    logging.debug("Exporting     sub group: %s", sub_ga)
                    ga_name = _format_ga_name(sub_ga)
                    ga_description = _format_ga_description(sub_ga)
                    writer.write_row(
                        [
                            ga_name,
                            f"{sub_ga.main}/{sub_ga.middle}/{sub_ga.sub}",
                            "",
                            "",
                            ga_description,
                            sub_ga.dpt,
                            "Auto",
                        ]
                    )


def _export_csv_format_3_3(
    output_file: str, output_file_encoding: str, csv_separator: str, group_addresses: list[GroupAddress]
) -> None:
    """Export KNX group address to CSV in format 'format_3_3'.

    Arguments:
        output_file: Path of output file
        output_file_encoding: Output file encoding
        csv_separator: CSV separator
        group_addresses: KNX group addresses
    """
    with open(output_file, "w", newline="", encoding=output_file_encoding) as csv_file:
        writer = CsvWriter(file=csv_file, delimiter=csv_separator, quoting=csv.QUOTE_ALL)

        # write headline
        writer.write_row(
            [
                "Main",
                "Middle",
                "Sub",
                "Main",
                "Middle",
                "Sub",
                "Central",
                "Unfiltered",
                "Description",
                "DatapointType",
                "Security",
            ]
        )

        main_group_ids = {ga.main for ga in group_addresses}
        for main_group_id in main_group_ids:
            filtered_main_gas = _filter_by_main_id(group_addresses, main_group_id)
            main_group_name = filtered_main_gas[0].main_name

            logging.debug("Exporting main group %s: %s", main_group_id, main_group_name)
            writer.write_row([main_group_name, "", "", main_group_id] + [""] * 6 + ["Auto"])

            middle_group_ids = {ga.middle for ga in filtered_main_gas}
            for middle_group_id in middle_group_ids:
                filtered_middle_gas = _filter_by_middle_id(filtered_main_gas, middle_group_id)
                middle_group_name = filtered_middle_gas[0].middle_name

                logging.debug("Exporting middle group %s/%s: %s", main_group_id, middle_group_id, middle_group_name)
                writer.write_row(["", middle_group_name, "", main_group_id, middle_group_id] + [""] * 5 + ["Auto"])

                for sub_ga in filtered_middle_gas:
                    logging.debug("Exporting sub group: %s", sub_ga)
                    ga_name = _format_ga_name(sub_ga)
                    ga_description = _format_ga_description(sub_ga)
                    writer.write_row(
                        [
                            "",
                            "",
                            ga_name,
                            sub_ga.main,
                            sub_ga.middle,
                            sub_ga.sub,
                            "",
                            "",
                            ga_description,
                            sub_ga.dpt,
                            "Auto",
                        ]
                    )


def _format_ga_name(ga: GroupAddress) -> str:
    """Format a KNX group address name.

    Args:
        ga: KNX group address

    Returns:
        Formatted name
    """
    ga_name = ga.sub_name
    if ga.target_id is not None and ga.target_id != 0:
        ga_name = ga.target_id + " - " + ga_name
        ga_name = ga_name.replace("\n", "_")
    return ga_name


def _format_ga_description(ga: GroupAddress) -> str:
    """Format a KNX group address description.

    Args:
        ga: KNX group address.

    Returns:
        Formatted description
    """
    description = ga.comment
    # Replace line-breaks
    if description is not None:
        description = description.replace("\n", "|")
    return description
