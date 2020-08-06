# -*- coding: utf-8 -*-

import copy
import os
import re
import sys

# Read and process Excel spreadsheets, converting Old Osage encoding into
# Unicode characters.

# Warning: Specialized to expect Old Osage text in column B.

# https://openpyxl.readthedocs.io/en/default/tutorial.html

#from openpyxl import Workbook
import openpyxl
from openpyxl import load_workbook

import convertUtil
import osageConversion
import quinteroConversion

debug = False  #True

# TIMESTAMP for version information.
TIMESTAMP = "Version 2018-01-25 20:30"

# Font names:
OfficialOsageFont = 'Official Osage Language'
SiDulosFont = 'Doulos SIL'

# Rule for detecting Latin text or Old Osage font.
# Some Old Osage text is in Latin CAPS, but with lower case a, e, and o.
latinOsagePattern2 = r'[\^A-Z\[\]][A-Zaeo; \[\]\^\\\'\/\._`,!]+'

# This identifies traditional Osage private use characters
traditionalOsageCharacters = r'([\uf020-\uf05e]+)'

# To avoid converting English words
notOsageLatinLower = re.compile(r'[b-df-np-z]')

osageConvertPattern = latinOsagePattern2 + '|' + traditionalOsageCharacters

def replFunc(matchObj):
  if matchObj.group(0):
    if notOsageLatinLower.search(matchObj.group(0)):
      return matchObj.group(0)
    else:
      return osageConversion.oldOsageToUnicode(matchObj.group(0))

# Check for Osage text and convert the Osage parts of the strings.
def checkAndConvertText(textIn):

  if textIn[0] == '=':
    # Ignore function calls
    return textIn
  #if notOsageLatinLower.search(textIn):
  #  return textIn

  # Handle Latin and TraditionalOsage private use characters.
  tryResult = osageConversion.oldOsageToUnicode(textIn)
  #tryResult = re.subn(osageConvertPattern, replFunc, textIn)
  #if tryResult[1] >= 1:
  return tryResult #[0]
  #else:
  #  return textIn


def convertSheet(ws, unicodeFont):
  print('\n  Converting sheet: %s' % ws)
  numConverts = 0
  notConverted = 0
  rowNum = 1
  for row in ws.rows:
    col = 0

    for cell in row:
      thisText = cell.value
      if not thisText:
        continue

      if debug:
        print('Cell (%d, %d) = >%s<  font = %s' % (rowNum, col, cell.value, cell.font.name))
      thisFont = cell.font
      if thisFont:
        convertedText = thisText
        if thisFont.name == OfficialOsageFont:
          convertedText = checkAndConvertText(thisText)
        elif thisFont.name == SiDulosFont:
          convertedText = quinteroConversion.quiteroOsageToUnicode(thisText)[0]
          print('*******QUINTERO Cell (%d, %d) CONVERTED %s to %s' % (
            rowNum, col, thisText, convertedText))
        if thisText != convertedText:
          converted = True
          numConverts += 1
          cell.value = convertedText
          newFont = copy.copy(thisFont)
          newFont.name = unicodeFont
          cell.font = newFont
          if debug:
            print('  Conversion = %s' % convertedText.encode('utf-8'))
        else:
          converted = False
          notConverted += 1

        # This is specific for Osage text in column B.
        # if not converted and col == 2:
        #   print( '**** NOT CONVERTED **** %s, %s' % (rowNum, cell.value))

      col += 1
      rowNum += 1
  print('    %d values converted to Unicode' % numConverts)
  return (numConverts, notConverted)


def convertAllSheets(wb, unicodeFont):
  totalConversions = 0

  for ws in wb.worksheets:
    (converted, notConverted) = convertSheet(ws, unicodeFont)
    totalConversions += converted

  return totalConversions


def processOneSpreadsheet(path_to_spreadsheet, output_dir,
                          unicodeFont='Pawhuska'):
  print('PATH = %s' % path_to_spreadsheet)
  wb = load_workbook(path_to_spreadsheet)

  print('Converting Osage in file: %s' % path_to_spreadsheet)

  print('TIMESTAMP: convertDoc: %s, osageConversion: %s' % (
      TIMESTAMP, osageConversion.TIMESTAMP))

  numConverts = convertAllSheets(wb, unicodeFont)

  if numConverts:
    newName = os.path.splitext(path_to_spreadsheet)[0]
    if output_dir is not '':
      fileIn = os.path.split(path_to_spreadsheet)[1]
      baseWOextension = os.path.splitext(fileIn)[0]
      unicode_path_to_spreadsheet = os.path.join(
          output_dir, baseWOextension + '_unicode.xlsx')
    else:
      baseWOextension = os.path.splitext(path_to_spreadsheet)[0]
      unicode_path_to_spreadsheet = os.path.join(
          output_dir, baseWOextension + '_unicode.xlsx')
    wb.save(unicode_path_to_spreadsheet)
    print('Saved new version to file %s' % unicode_path_to_spreadsheet)
  else:
    print('  No conversion done, so no new file croeated.')


def main(argv):
  args = convertUtil.parseArgs()

  paths_to_spreadsheet = args.filenames

  print('files to process = %s' % paths_to_spreadsheet)

  convertFileCount = 0

  for path in paths_to_spreadsheet:
    processOneSpreadsheet(path, args.output_dir, args.font)
    convertFileCount += 1

  print('\n%d files processed' % convertFileCount)


if __name__ == "__main__":
  main(sys.argv)
