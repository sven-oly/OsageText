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

import convertDoc

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

def parseDocXMLText(path_to_doc, unicodeFont='Pawhuska',
                saveConversion=False, outpath=None, isString=False):
  if isString:
    tree = ET.fromstring(path_to_doc)
    #tree = ET.parse(path_to_doc)
    root = tree
  else:
    tree = ET.parse(path_to_doc)
    root = tree.getroot()

  # TODO: Complete this.
  print ('Looking for drawing:')
  drawingCount = 0
  for p in tree.getiterator():
    if re.search('}drawing', p.tag):
      drawingCount += 1
      print (p)
  print ('%d drawing lines found' % drawingCount)
  print ('----------------------------')

  if drawingCount == 0:
    convertWordOsage.convertOneDoc(path_to_doc)
    return

  # So we can get the parents of each node.
  # http://elmpowered.skawaii.net/?p=74
  parent_map = dict((c, p) for p in tree.getiterator() for c in p)

  body = root.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body')

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
                  if convertDoc.isOsageFontNode(rprchild):
                    # In font encoded node
                    inEncodedFont = True
                  else:
                    # Check if we are switching out. If so, handle accumulated text
                    if inEncodedFont:
                      if collectedText:
                        convertCount += convertDoc.processCollectedText(collectedText,
                                                             textElements, parent_map,
                                                             superscriptNode,
                                                             unicodeFont=unicodeFont)
                      collectedText = ''
                      textElements = []
                      inEncodedFont = False
            if re.search('}t', rchild.tag):
              if inEncodedFont:
                # Process <w:t>
                collectedText += rchild.text
                textElements.append(rchild)
              else:
                print '**** not encoded: >%s' % rchild.text

  if collectedText:
    convertCount += convertDoc.processCollectedText(collectedText, textElements,
                                                    parent_map, superscriptNode,
                                                    unicodeFont=unicodeFont)
    collectedText = ''
    textElements = []

  print '%d text items converted' % convertCount

  if isString:
    return ET.tostring(root, encoding='utf-8')

  if saveConversion:
    if not outpath:
      outpath = path_to_doc
    tree.write(outpath)
  return tree, convertedList
