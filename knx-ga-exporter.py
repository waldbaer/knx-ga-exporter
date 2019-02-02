#!/usr/bin/env python3

import logging
import sys
import traceback
import argparse
from openpyxl import load_workbook
import csv

# ---- Main ------------------------------------------------------------------------------------------------------------
class GroupAddress:
  def __init__(self, main, middle, sub, main_name, middle_name, sub_name, target_id, dpt, comment):
    self.main=main
    self.middle=middle
    self.sub=sub
    self.main_name=main_name
    self.middle_name=middle_name
    self.sub_name=sub_name
    self.target_id=target_id
    self.dpt=dpt
    self.comment=comment
  def __str__(self):
    return '{}/{}/{} {}|{}|{}'.format(self.main, self.middle, self.sub, self.main_name, self.middle_name, self.sub_name)

def main():
  args = ParseCommandLineArguments()
  logging.basicConfig(level=logging.DEBUG)

  wb = LoadWorkbook(args.input_file)
  gas = ParseGroupAddresses(wb, args)
  ExportCsv(gas, args.output_file)

  logging.info("Statistics: #GA: {}".format(len(gas)))
  logging.info('done.')

def ParseCommandLineArguments():
  parser = argparse.ArgumentParser(description='KNX group address exporter.')
  parser.add_argument('-i', '--input', dest='input_file', required=True, help='Path to XSLX file to be parsed.')
  parser.add_argument('-o', '--output', dest='output_file', required=False, default='knx-ga-addresses.csv', help='Path of exported CSV file.')

  parser.add_argument('--ga-sheet-name', default='KNX-Gruppenadressen', help='Name of XLSX sheet containing the KNX group addresses')
  parser.add_argument('--ga-sheet-first-row', default=8, help='First row containing GAs')
  parser.add_argument('--ga-sheet-last-column', default=10, help='Last column')

  parser.add_argument('--ga-sheet-main-ID-column', default=0, help='Column containing main ID of KNX GA')
  parser.add_argument('--ga-sheet-middle-ID-column', default=2, help='Column containing middle ID of KNX GA')
  parser.add_argument('--ga-sheet-sub-ID-column', default=4, help='Column containing sub ID of KNX GA')

  parser.add_argument('--ga-sheet-main-name-column', default=1, help='Column containing main name of KNX GA')
  parser.add_argument('--ga-sheet-middle-name-column', default=3, help='Column containing middle name of KNX GA')
  parser.add_argument('--ga-sheet-sub-name-column', default=8, help='Column containing sub name of KNX GA')

  parser.add_argument('--ga-sheet-dpt-column', default=5, help='Column containing datapoint type of KNX GA')
  parser.add_argument('--ga-sheet-target-ID-column', default=6, help='Column containing target ID KNX GA')
  parser.add_argument('--ga-sheet-compiled-GA-column', default=7, help='Column containing full accumulated GA')
  parser.add_argument('--ga-sheet-comment', default=9, help='Column containing GA comment')

  args = parser.parse_args()
  return args

def LoadWorkbook(input_file):
  logging.info("Loading XLSX input file '{}'".format(input_file))
  wb = load_workbook(filename=input_file, read_only=True, data_only=True)
  return wb

def ParseGroupAddresses(wb, args):
  gas = []
  ws = wb[args.ga_sheet_name]
  for row in ws.iter_rows(min_row=args.ga_sheet_first_row, max_col=args.ga_sheet_last_column):
    target_id = row[args.ga_sheet_target_ID_column].value

    group_main = row[args.ga_sheet_main_ID_column].value
    group_middle = row[args.ga_sheet_middle_ID_column].value
    group_sub = row[args.ga_sheet_sub_ID_column].value

    group_main_name = row[args.ga_sheet_main_name_column].value
    group_middle_name = row[args.ga_sheet_middle_name_column].value
    group_sub_name = row[args.ga_sheet_sub_name_column].value

    dpt = row[args.ga_sheet_dpt_column].value
    compiled_ga = row[args.ga_sheet_compiled_GA_column].value
    comment = row[args.ga_sheet_comment].value

    # Skip invalid / incomplete GAs
    if(dpt == None or dpt == 0 or compiled_ga == None or compiled_ga == 0):
      continue

    ga = GroupAddress(group_main, group_middle, group_sub, group_main_name, group_middle_name, group_sub_name, target_id, dpt, comment)
    logging.info("Parsed GA: %s" % (str(ga)))
    gas.append(ga);
  return gas

def ExportCsv(gas, output_file):
  logging.info("Exporting group addresses into CSV file '{}'".format(output_file))
  with open(output_file, 'w', newline='', encoding='iso-8859-1') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)

    # write headline
    writer.writerow(['Main', 'Middle', 'Sub', 'Main', 'Middle', 'Sub', 'Central', 'Unfiltered', 'Description', 'DatapointType','Security'])

    main_group_ids = {ga.main for ga in gas}
    for main_group_id in main_group_ids:
      filtered_main_gas = list(filter(lambda ga: ga.main == main_group_id, gas))
      main_group_name = filtered_main_gas[0].main_name

      logging.info("Exporting main group {}: {}".format(main_group_id, main_group_name))
      writer.writerow([main_group_name, '', '', main_group_id] + [''] * 6 + ['Auto'])

      middle_group_ids = {ga.middle for ga in filtered_main_gas}
      for middle_group_id in middle_group_ids:
        filtered_middle_gas = list(filter(lambda ga: ga.middle == middle_group_id, filtered_main_gas))
        middle_group_name = filtered_middle_gas[0].middle_name

        logging.info("Exporting middle group {}/{}: {}".format(main_group_id, middle_group_id, middle_group_name))
        writer.writerow(['', middle_group_name, '', main_group_id, middle_group_id] + [''] * 5 + ['Auto'])

        for sub_ga in filtered_middle_gas:
          logging.info("Exporting sub group: {}".format(sub_ga))
          ga_name = FormatGaName(sub_ga)
          ga_description = FormatGaDescription(sub_ga)
          writer.writerow(['', '', ga_name, sub_ga.main, sub_ga.middle, sub_ga.sub, '', '', ga_description, sub_ga.dpt, 'Auto'])

def FormatGaName(ga):
  ga_name = ga.sub_name
  if(ga.target_id != None and ga.target_id != 0):
    ga_name = ga.target_id + " - " + ga_name
  return ga_name

def FormatGaDescription(ga):
  return ga.comment

# ---- Entrypoint ------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
  try:
    main()
  except SystemExit:
    sys.exit(1)
  except BaseException:
    logging.error("Any error has occured! Traceback:\r\n" + traceback.format_exc())
    sys.exit(1)
  sys.exit(0)
