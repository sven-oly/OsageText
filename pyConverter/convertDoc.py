# -*- coding: utf-8 -*-

import os
import re
import sys
import zipfile

import xml.etree.ElementTree as ET

import convertUtil
import osageConversion

# The version using docx
import convertWordOsage

# TIMESTAMP for version information.
TIMESTAMP = "Version 2017-12-20 07:55"

# Documentation here:
# https://docs.python.org/2/library/xml.etree.elementtree.html
# https://docs.python.org/2/library/zipfile.html

# https://python-docx.readthedocs.io/en/latest/user/text.html

# Font names:
OfficialOsageFont = 'Official Osage Language'
FONTS_TO_CONVERT = [OfficialOsageFont]

debug_output = False

# Flag controls if the conversion removes
# structure from replaced text when drawings are found
# in the .docx input.
removeOldText = False
# More aggressive removal of grandparents of empty text blocks.
removeOldTextParents = False

# If enabled, replaces the Official Osage font in fontsTable.xml
convertFontsTable = False

def fixElementAndParent(textElement, parent, newText, unicodeFont):
  removeList = []
  oldText = textElement.text
  for item in parent.findall('*'):
    for child in item.findall('*'):
      if re.search('}rFonts', child.tag):
        attrib = child.attrib
        for key in attrib:
          if attrib[key] == OfficialOsageFont:
            attrib[key] = unicodeFont
      elif re.search('}vertAlign', child.tag):
        if (oldText == u'H' or oldText == u'\uf048'):
          keys = child.attrib.keys()
          if re.search('}val', keys[0]):
            child.attrib[keys[0]] = 'baseline'

  textElement.text = newText


# Replace the text in the first text element with the converted
# unicode string, remove text from other text elements in that,
# batch, and remove the empty elements.
# Should I reset the font in this function, too?
def processCollectedText(collectedText, textElementList, parent_map, superscriptNode,
                         unicodeFont):
  clearedTextElements = []
  global debug_output

  # First, change the text
  if debug_output:
    print('** CONVERTING %s to Unicode. ' % collectedText.encode('utf-8'))
  convertedText = osageConversion.oldOsageToUnicode(collectedText)
  convertedCount = 0
  if convertedText != collectedText:
    convertedCount = 1
  else:
    print('---- Not converted: %s' % collectedText.encode('utf-8'))

  # 1. Reset text in first element
  if not textElementList:
    return 0
    # ∂textElementList[0].text = convertedText
  parent = parent_map[textElementList[0]]
  # Fix font and superscripting
  fixElementAndParent(textElementList[0], parent, convertedText, unicodeFont)  # Update the font in this item.
  if superscriptNode:
    superscriptNode.val = 'baseline'

  # 2. Clear text in other elements
  for element in textElementList[1:]:
    element.text = ''
    clearedTextElements.append(element)

  return convertedCount, clearedTextElements

# Looks at text parts of the DOCX data, extracting each.
def parseDocXML(docfile_name, path_to_doc, unicodeFont='Pawhuska',
                saveConversion=False, outpath=None, isString=False):
  global debug_output
  if isString:
    tree = ET.fromstring(path_to_doc)
    root = tree
  else:
    tree = ET.parse(path_to_doc)
    root = tree.getroot()

  drawingCount = 0
  for p in tree.getiterator():
    if re.search('}drawing', p.tag):
      drawingCount += 1

  if debug_output:
    print ('%d drawing lines found' % drawingCount)

  if drawingCount == 0 and docfile_name == 'word/document':
    convertWordOsage.convertOneDoc(path_to_doc)
    return

  # So we can get the parents of each node.
  # http://elmpowered.skawaii.net/?p=74
  parent_map = dict((c, p) for p in tree.getiterator() for c in p)

  # TODO: package the following in a separate function
  convertCount = 0

  allEmptiedTextElements = []
  # Look for series of items
  textElements = []
  collectedText = ''
  superscriptNode = False

  # Current font
  inEncodedFont = False
  fontFound = False

  for node in root.iter('*'):

    if re.search('}p$', node.tag):

      textElements = []
      collectedText = ''
      superscriptNode = False
      inEncodedFont = False

      # Process the children.
      for pchild in node._children:
        if re.search('}r$', pchild.tag):
          # Look at the rPr and <w:t>

          for rchild in pchild._children:
            superscriptNode = None

            # Process <w:r>
            if re.search('}rPr', rchild.tag):
              fontFound = False
              for rprchild in rchild._children:
                # Process <w:rPr>
                if re.search('}vertAlign', rprchild.tag):
                  superscriptNode = rprchild
                elif re.search('}rFonts', rprchild.tag):
                  # Font info.
                  fontFound = True
                  if isOsageFontNode(rprchild):
                    # In font encoded node
                    inEncodedFont = True
                  else:
                    # Check if we are switching out. If so, handle accumulated text
                    if inEncodedFont:
                      if collectedText:
                        (newConvertedCount, emptiedElements) = (
                          processCollectedText(collectedText,
                                               textElements, parent_map,
                                               superscriptNode,
                                               unicodeFont=unicodeFont))
                        convertCount += newConvertedCount
                        allEmptiedTextElements.append(emptiedElements)
                      collectedText = ''
                      textElements = []
                      inEncodedFont = False
            elif re.search('}t', rchild.tag):
              if not fontFound and debug_output:
                print('^^^^^^^^^^^^^ Font not found ^^^^')
              if fontFound and inEncodedFont and rchild.text:
                # Process <w:t>
                collectedText += rchild.text
                textElements.append(rchild)
              else:
                notEncoded = rchild.text
                if notEncoded and debug_output:
                  print 'notEncoded = >%s<' % notEncoded.encode('utf-8')

    if collectedText:
      (newConvertedCount, emptiedElements) = (
        processCollectedText(collectedText,
                             textElements, parent_map, superscriptNode,
                             unicodeFont=unicodeFont))
      convertCount += newConvertedCount
      collectedText = ''
      textElements = []
      allEmptiedTextElements.append(emptiedElements)

  # TODO: remove all emptied text elements.
  removeOldTextElements(allEmptiedTextElements, parent_map)

  print ' %s: %d text items converted' % (docfile_name, convertCount)

  if isString:
    return ET.tostring(root, encoding='utf-8')

  if saveConversion:
    if not outpath:
      outpath = path_to_doc
    tree.write(outpath)
  return tree


def removeOldTextElements(allElementsToRemove, parent_map):
  count = 0

  if not removeOldText:
    return count

  # This may be causing corruption in the MS Word file structure.
  for group in reversed(allElementsToRemove):
    for item in  reversed(group):
      parent = parent_map[item]
      parent.remove(item)

      if not removeOldTextParents:
        continue
     # Can I remove the parent of this, too?
      grandparent = parent_map[parent]
      if grandparent is not None:
        grandparent.remove(parent)
      count += 1

  # And probably remove the siblings and the empty parent, too.
  print 'removed %d items' % count
  return count

def isOsageFontNode(node):
  # Look for "rFonts", and check if any font contains "Official Osage"
  if re.search('}rFonts', node.tag):
    for key in node.attrib:
      if re.search('Official Osage', node.attrib[key]):
        return True
  return False


def parseFontTable(docXML, unicodeFont):
  tree = ET.fromstring(docXML)

  for node in tree.iter('*'):
    if re.search('}font$', node.tag):
      keys = node.attrib.keys()
      if re.search('}name', keys[0]) and node.attrib[keys[0]] == OfficialOsageFont:
        print 'Replacing font %s with %s' % (node.attrib[keys[0]], unicodeFont)
        node.attrib[keys[0]] = unicodeFont
  return ET.tostring(tree, encoding='utf-8')


def tryFontUpdate(newzip, unicodeFont):
  filename = 'word/fontTable.xml'
  docXML = newzip.read(filename)  # A file-like object

  return parseFontTable(docXML, unicodeFont)


def processDOCX(path_to_doc, output_dir, unicodeFont='Pawhuska', debug=False):
  global debug_output

  print 'TIMESTAMP: convertDoc: %s, osageConversion: %s' % (
      TIMESTAMP, osageConversion.TIMESTAMP)

  newzip = zipfile.ZipFile(path_to_doc)
  docfiles = ['word/document.xml', 'word/header1.xml', 'word/footer1.xml']
  docPartsOut = {}

  if convertFontsTable:
    newFontTable = tryFontUpdate(newzip, unicodeFont)
    docPartsOut['word/fontTable.xml'] = newFontTable

  for docfile_name in docfiles:

    compress_method = ''
    for info in newzip.infolist():
      if info.filename == docfile_name:
        compress_method = info.compress_type

    if debug_output:
      print 'COMPRESS TYPE = %s' % compress_method

    try:
      docXML = newzip.read(docfile_name)  # A file-like object
    except KeyError:
      continue

    # The real parsing.
    new_docXML = parseDocXML(docfile_name, docXML, unicodeFont, isString=True)
    # Remember this piece for output.
    docPartsOut[docfile_name] = new_docXML

  # All done with the pieces. Now create a new zip archive to save it.
  if output_dir is not '':
    # String the directory tree to the file, substituting the output
    fileIn = os.path.split(path_to_doc)[1]
    baseWOextension = os.path.splitext(fileIn)[0]
  else:
    baseWOextension = os.path.splitext(path_to_doc)[0]
  outpath = os.path.join(output_dir, baseWOextension + '_unicode.docx')
  outzip = zipfile.ZipFile(outpath, 'w')  #, compress_method)

  print '  OUTPATH = %s' % outpath

  # copy other things
  for info in newzip.infolist():
    if info.filename not in docPartsOut:
      copyfile = newzip.read(info.filename)
      outzip.writestr(info, copyfile)
      if debug_output:
        print '  COPY %s' % info.filename
    else:
      # Skipping the new data for now.
      outzip.writestr(info, docPartsOut[info.filename])
      if debug_output:
        print 'Adding %s' % info.filename

  if debug_output:
    outzip.printdir()
  outzip.comment = newzip.comment + ' Updated to Unicode text'
  outzip.close()


def unzipInputFile(infile, outdir):
  # https://docs.python.org/3/library/zipfile.html
  print 'unzipping %s to directory %s' % (infile, outdir)

  newzip = zipfile.ZipFile(infile)
  result = newzip.extractall(path=outdir, pwd=None)
  print 'zip extract result = %s' % result

  return newzip


def main(argv):
  global debug_output

  args = convertUtil.parseArgs()

  paths_to_doc = args.filenames
  print 'ARGS = %s' % args

  print('Args = %s'% args.debug)

  for path in paths_to_doc:
    extension = os.path.splitext(path)[-1]
    if extension == '.docx':
      processDOCX(path, args.output_dir, args.font, debug_output)
    else:
      print '!!! Not processing file %s !' % path


if __name__ == "__main__":
  main(sys.argv)
