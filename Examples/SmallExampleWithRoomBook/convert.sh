#!/bin/bash
set -e

# ---- config ----
CONVERTER_BIN=../../knx-ga-exporter.py
XLSX=./KNX-planning-example.xlsx
CSV_OUTPUT=./knx-group-addresses.csv

# ---- run ----
$CONVERTER_BIN -i $XLSX -o $CSV_OUTPUT
