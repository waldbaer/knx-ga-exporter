#!/bin/bash
set -e

# ---- config ----
INPUT_SHEET=./KNX-planning-example.xlsx
CSV_OUTPUT=./knx-group-addresses.csv

# ---- run ----
knx-ga-exporter --input ${INPUT_SHEET} --output ${CSV_OUTPUT} --verbose
