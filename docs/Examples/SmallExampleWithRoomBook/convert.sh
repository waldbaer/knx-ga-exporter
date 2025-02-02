#!/bin/bash
set -e

# ---- config ----
INPUT_SHEET=./KNX-planning-example.xlsx
CSV_OUTPUT=./knx-group-addresses.csv

# ---- run ----
knx-ga-exporter --input.file ${INPUT_SHEET} --output.file ${CSV_OUTPUT} -vv
