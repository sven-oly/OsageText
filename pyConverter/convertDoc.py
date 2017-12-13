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

import docxDebug

# https://docs.python.org/2/library/xml.etree.elementtree.html
# https://docs.python.org/2/library/zipfile.html

# Font names:
OfficialOsageFont = 'Official Osage Language'
FONTS_TO_CONVERT = [OfficialOsageFont]

# Rule for detecting Latin text or Old Osage font.
# Some Old Osage text is in Latin CAPS, but with lower case a, e, and o.
latinOsagePattern2 = ur'[\^A-Z\[\]][A-Zaeo\[\]\^\\\'\/\._`,!]+'

# This identifies traditional Osage private use characters
traditionalOsageCharacters = ur'([\uf020-\uf05e]+)'

# To avoid converting English words
notOsageLatinLower = re.compile(r'[b-df-np-z]')

osageConvertPattern = latinOsagePattern2 + '|' + traditionalOsageCharacters

debug_output = False

debugParse = False  # Remove when no longer needed

def replFunc(matchObj):
  if matchObj.group(0):
    if notOsageLatinLower.search(matchObj.group(0)):
      return matchObj.group(0)
    else:
      return osageConversion.oldOsageToUnicode(matchObj.group(0))

# Check for Osage text and convert the Osage parts of the strings.
def checkAndConvertText(textIn):
  if not textIn:
    return textIn

  if textIn[0] == '=':
    # Ignore function calls
    return textIn
#  if notOsageLatinLower.search(textIn):
#    return textIn

  # Handle Latin and TraditionalOsage private use characters.
  tryResult = re.subn(osageConvertPattern, replFunc, textIn)
  if tryResult[1] >= 1:
    return tryResult[0]
  else:
    return textIn


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
  # TODO:
  # First, change the text
  if debug_output:
    print('** CONVERTING %s to Unicode. ' % collectedText)
  convertedText = osageConversion.oldOsageToUnicode(collectedText)
  convertedCount = 0
  if convertedText != collectedText:
    convertedCount = 1
  else:
    print('---- Not converted: %s' % collectedText)

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

  # Try removing these empty text parents.
  # for parent in oldTextParentList:
  #  uP = parent_map[parent]
  #  if uP and parent:
  #    uP.remove(parent)
  # 3. Delete empty elements:
  # Maybe this is nuking too much.
  # for uP in uberParents:
  #   uPP = parent_map[uP]
  #   if uPP and uP:
  #     uPP.remove(uP)
  return convertedCount

# Looks at text parts of the DOCX data, extracting each.
def parseDocXML(docfile_name, path_to_doc, unicodeFont='Pawhuska',
                saveConversion=False, outpath=None, isString=False):
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
  osageNodeCount = 0
  convertCount = 0

  # Look for series of items
  textElements = []
  collectedText = ''

  # Current font
  inEncodedFont = False

  for node in root.iter('*'):

    if re.search('}p$', node.tag):

      textElements = []
      collectedText = ''
      superscriptNode = False

      # Process the children.
      for pchild in node._children:
        if re.search('}r$', pchild.tag):
          # Look at the rPr and <w:t>

          for rchild in pchild._children:
            superscriptNode = None

            # Process <w:r>
            if re.search('}rPr', rchild.tag):
              for rprchild in rchild._children:
                # Process <w:rPr>
                if re.search('}vertAlign', rprchild.tag):
                  # TODO: Handle the superscript flag
                  superscriptNode = rprchild
                elif re.search('}rFonts', rprchild.tag):
                  # Font info.
                  if isOsageFontNode(rprchild):
                    # In font encoded node
                    inEncodedFont = True
                  else:
                    # Check if we are switching out. If so, handle accumulated text
                    if inEncodedFont:
                      if collectedText:
                        convertCount += processCollectedText(collectedText,
                                                             textElements, parent_map,
                                                             superscriptNode,
                                                             unicodeFont=unicodeFont)
                      collectedText = ''
                      textElements = []
                      inEncodedFont = False
            elif re.search('}t', rchild.tag):
              if inEncodedFont:
                # Process <w:t>
                collectedText += rchild.text
                textElements.append(rchild)
              else:
                notEncoded = rchild.text
                # print 'notEncoded = >%s<' % notEncoded

    if collectedText:
      convertCount += processCollectedText(collectedText, textElements, parent_map, superscriptNode,
                                           unicodeFont=unicodeFont)
      collectedText = ''
      textElements = []

  print ' %s: %d text items converted' % (docfile_name, convertCount)

  if isString:
    return ET.tostring(root, encoding='utf-8')

  if saveConversion:
    if not outpath:
      outpath = path_to_doc
    tree.write(outpath)
  return tree, convertedList


def isOsageFontNode(node):
  # Look for "rFonts", and check if any font contains "Official Osage"
  if re.search('}rFonts', node.tag):
    for key in node.attrib:
      if re.search('Official Osage', node.attrib[key]):
        return True
  return False


def processDOCX(path_to_doc, output_dir, unicodeFont='Pawhuska'):
  newzip = zipfile.ZipFile(path_to_doc)
  docfiles = ['word/document.xml', 'word/header1.xml', 'word/footer1.xml']

  docPartsOut = {}
  for docfile_name in docfiles:

    compress_method = ''
    for info in newzip.infolist():
      if info.filename == docfile_name:
        compress_method = info.compress_type

    if debug_output:
      print 'COMPRESS TYPE = %s' % compress_method

    docXML = newzip.read(docfile_name)  # A file-like object

    if debugParse:
      docxDebug.parseDocXMLText(docXML, unicodeFont, isString=True)
      # For debugging the parsing only
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
  # Be careful on this.
  result = newzip.extractall(path=outdir, pwd=None)
  print 'zip extract result = %s' % result

  return newzip


def main(argv):
  args = convertUtil.parseArgs()

  paths_to_doc = args.filenames
  print 'ARGS = %s' % args

  for path in paths_to_doc:
    extension = os.path.splitext(path)[-1]
    if extension == '.docx':
      processDOCX(path, args.output_dir, args.font)
    else:
      print '!!! Not processing file %s !' % path


if __name__ == "__main__":
  main(sys.argv)
