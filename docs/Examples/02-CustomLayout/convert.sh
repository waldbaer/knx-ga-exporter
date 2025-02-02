#!/bin/bash
set -e

# ---- config ----
INPUT_SHEET=./custom-layout.xlsx
CONFIG_FILE=./custom-layout-config.json
CSV_OUTPUT=./custom-layout-knx-group-addresses.csv

# ---- run ----
knx-ga-exporter --config ${CONFIG_FILE} --input.file ${INPUT_SHEET} --output.file ${CSV_OUTPUT} -vv
