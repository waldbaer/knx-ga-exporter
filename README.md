[![MIT License](https://img.shields.io/github/license/waldbaer/knx-ga-exporter?style=flat-square)](https://opensource.org/licenses/MIT)
[![GitHub issues open](https://img.shields.io/github/issues/waldbaer/knx-ga-exporter?style=flat-square)](https://github.com/waldbaer/knx-ga-exporter/issues)


# KNX GroupAddress Exporter #
A simple converter for spreadsheets to KNX ETS group address configurations in CSV format.

Converter allows to use all possible features of the spreadsheet tools like Excel, LibreOffice etc to plan, duplicate and maintain your KNX group addresses. No more unhandy group address duplication or management in the KNX ETS software.

## Key features ##
 - Parse and convert Excel sheets to KNX ETS readable CSV files containing group address configuration.
 - Different KNX ETS CSV formats supported.

## Requirements ##
 - Python 3
 - [virtualenv](https://virtualenv.readthedocs.org/en/latest/)
 - [pip (package manager)](http://en.wikipedia.org/wiki/Pip_%28package_manager%29)
 - [openpyxl](https://pypi.org/project/openpyxl/)


## Setup ##
```
# Setup virtualenv
virtualenv -p python3 virtualenv3
source ./virtualenv3/bin/activate
# or
./setup-venv.h
```

## Usage ##

### Step1: Convert spreadsheet to ETS readable CSV file. ###
```
# Example usage.
knx-ga-exporter.py -i my-knx-planning.xlsx -o knx-group-addresses.csv

    INFO:root:Loading XLSX input file './my-knx-planning.xlsx'
    INFO:root:Parsed GA: 0/0/0 Light & Power|Switch|Basement Office - Ceiling light - Light & Power Switch
    INFO:root:Parsed GA: 0/0/1 Light & Power|Switch|Top Floor Bathroom - Ceiling light - Light & Power Switch
    INFO:root:Parsed GA: 0/0/2 Light & Power|Switch|Top Floor Bedroom - Wall light (north) - Light & Power Switch

    INFO:root:Statistics: #GA: 16
    INFO:root:done.

# CSV export can be found in knx-group-addresses.csv
cat knx-group-addresses.csv

"Group name"	"Address"	"Central"	"Unfiltered"	"Description"	"DatapointType"	"Security"
"Light & Power"	"0/-/-"	""	""	""	""	"Auto"
"Switch"	"0/0/-"	""	""	""	""	"Auto"
"B0-0-L - Basement Office - Ceiling light - Light & Power Switch"	"0/0/0"	""	""	""	"DPST-1-1"	"Auto"
"T0-0-L - Top Floor Bathroom - Ceiling light - Light & Power Switch"	"0/0/1"	""	""	""	"DPST-1-1"	"Auto"
"T1-0-L - Top Floor Bedroom - Wall light (north) - Light & Power Switch"	"0/0/2"	""	""	""	"DPST-1-1"	"Auto"

# More command line options are available
knx-ga-exporter.py --help
```

### Step2: Load CSV into KNX ETS application ###
* Open the KNX ETS application and the project.
* Edit -> Import Group Addresses -> Select the generated CSV file.
* Voila! New group addresses are added or existing addresses got renamed.

_Hint_: The KNX ETS application will not automatically delete group addresses not contained in the CSV file anymore. A cleanup must be done manually.

### Examples

Examples including the standard spreadsheet format can be found in folder `Examples`
