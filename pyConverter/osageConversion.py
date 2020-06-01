# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re

# Convert Osage text to Unicode.

# TIMESTAMP for version information.
TIMESTAMP = "Version 2020-05-28"

# TODO: resolve duplicates in the map.

debug = False

accent = u'\u0301'
doubleAccent = u'\u030B'
macron = u"\u0304"
combiningDotAboveRight = u'\u0358'
osageCaseOffset = 40  # Amount to add to get lower case from upper.
firstOsageUpper = 0x104B0
lastOsageUpper = 0x104D3

minOsageU = chr(0x104b0)
maxOsageU = chr(0x104d8)
lowerCaseOffset = 0x28
oldOsageDot = u'\uf02e'

osage_private_use_map = {
  u'\uf020': ' ',
  u'\uf021': '!',
  u'\uf022': chr(0x104c7),
  u'\uf023': '#',
  u'\uf024': '$',
  u'\uf025': '%',
  u'\uf026': '&',
  u'\uf027': "\'",
  u'\uf028': '(',
  u'\uf029': ')',
  u'\uf02a': '*',
  u'\uf02b': '+',
  u'\uf02c': chr(0x104ba),
  u'\uf02d': '-',
  u'\uf02e': '.',
  u'\uf02f': chr(0x104be),
  u'\uf030': '0',
  u'\uf031': '1',
  u'\uf032': '2',
  u'\uf033': '3',
  u'\uf034': '4',
  u'\uf035': '5',
  u'\uf036': '6',
  u'\uf037': '7',
  u'\uf038': '8',
  u'\uf039': '9',
  u'\uf03a': ':',
  u'\uf03b': chr(0x104C6) + chr(0x104BC),  # Character is no longer used.
  u'\uf03c': '<',
  u'\uf03d': '=',
  u'\uf03e': '>',
  u'\uf03f': chr(0x104be),
  u'\uf040': '@',
  u'\uf041\uf041': chr(0x104b0)+macron,
  u'\uf041^': chr(0x104b0)+combiningDotAboveRight,
  u'\uf041': chr(0x104b0),

  u'\uf041\uf05e': chr(0x104b0)+combiningDotAboveRight,
  u'\uf041\uf059': chr(0x104b1),
  u'\uf042': chr(0x104b4),
  u'\uf043': chr(0x104b5),
  u'\uf044': chr(0x104c8),
  u'\uf045\uf045': chr(0x104b7)+macron,
  u'\uf045^': chr(0x104b7)+combiningDotAboveRight,
  u'\uf045': chr(0x104b7),

  u'\uf045\uf05e': chr(0x104b7)+combiningDotAboveRight,
  u'\uf048': chr(0x104b9),
  # The eh-consonants
  u'\uf048\uf043': chr(0x104b6),
  u'\uf048\uf04b': chr(0x104bd),
  u'\uf048\uf050': chr(0x104c5),
  u'\uf048\uf044': chr(0x104c9),
  u'\uf048\uf05d': chr(0x104cb),
  
  u'\uf049': chr(0x104b1),
  u'\uf04a': chr(0x104b3),
  u'\uf04b': chr(0x104bc),
  u'\uf04c': chr(0x104bf),
  u'\uf04d': chr(0x104c0),
  u'\uf04e': chr(0x104c1),
  u'\uf04f^': chr(0x104c2)+combiningDotAboveRight,
  u'\uf04f\uf04f': chr(0x104c2)+macron,
  u'\uf04f': chr(0x104c2),
  u'\uf04f\uf05e': chr(0x104c2)+combiningDotAboveRight,
  u'\uf050': chr(0x104c4),
  u'\uf051': ' ',  # Space characters
  u'\uf052': ' ',
  u'\uf053': chr(0x104c6),
  u'\uf054': chr(0x104cd),
  u'\uf055\uf055': chr(0x104ce)+macron,
  u'\uf055': chr(0x104ce),
  u'\uf055\uf05e': chr(0x104ce)+combiningDotAboveRight,
  u'\uf056': chr(0x104c7),
  u'\uf057': chr(0x104cf),
  u'\uf058': chr(0x104d0),
  u'\uf059': chr(0x104bb),
  u'\uf059^': chr(0x104bb)+combiningDotAboveRight,
  u'\uf059\uf059': chr(0x104bb)+macron,
  u'\uf059\uf05e': chr(0x104bb)+combiningDotAboveRight,
  u'\uf05a': chr(0x104d2),  # ??
  u'\uf05b': chr(0x104d3),  # ??
  u'\uf05c': chr(0x104c6) + chr(0x104c8),  # Character is no longer used.
  u'\uf05d': chr(0x104ca),  # ??],
  u'\uf05e': combiningDotAboveRight,  # '^',  # '^',
  u'\uf05f': '_',
  u'\uf060': '`',
  u'\uf061': chr(0x104b2),
  u'\uf061\uf061': chr(0x104b2) + macron,
  u'\uf065': chr(0x104b8),
  u'\uf065\uf065': chr(0x104b8) + macron,
  u'\uf06a': ' ',
  u'\uf06b': ' ',
  u'\uf06c': ' ',
  u'\uf06d': ' ',
  u'\uf06e': ' ',
  u'\uf06f': chr(0x104c3),
  u'\uf06f\uf06f': chr(0x104c3) + macron,
  u'\uf07b': '{',
  u'\uf07c': '|',
  u'\uf07d': '}',
  u'\uf07e': '~',
  u'\uf0b6': '\u00b6',
  # Some older combination codes
  u'\ue000': chr(0x104b0) + combiningDotAboveRight,

  u'\u2026': u'\u2026',
}

osage_latin_to_unicode_map = {
  u'\u0020': ' ',
  u'\u0027': '\'',
  u'\u0029': ')',
  u'\u002f': chr(0x104be),
  u'\u0031': '1',
  u'\u004f': chr(0x104c2),

  # Not sure what is the Osage script for these
  u'\u00e6': chr(0x207f),  # n superscript
  u'\u00be': chr(0x1ed6),  # t dot below
  u'\u00d0': chr(0x1e32),  # k dot below
  u'\u00e3': chr(0x0263),  # latin gamma
  u'\u00ec': chr(0x02db),  # i ogonek
  u'\u00c7': chr(0x0161),  # s + caron
  u'\u00f4': chr(0x01eb) + chr(0x0301),  # o acute ogonek
  u'\u00e2': chr(0x0105) + chr(0x0301),  # a acute ogonek
  u'\u00f2': chr(0x01eb),  # o ogonek
  u'\u00d8': chr(0x02c0),  # glottal stop
  u'\u00eb': chr(0x0171),  # z + caron

  'ì': 'i' + chr(0x0328),  #

  'á': chr(0x104d8) + accent,
  'a': chr(0x104b2),
  'aa': chr(0x104d8)+ macron,
  'ā': chr(0x104d8)+ macron,
  'ą̄': chr(0x104d8)+ macron,
  'a\'': chr(0x104d9),
  'b':  chr(0x104dc),
  'br': chr(0x104dc),
  'hc': chr(0x104de),
  'c':  chr(0x104dd),
  'ch': chr(0x104de),
  'd':  chr(0x104f0),
  'é':  chr(0x104df) + accent,
  'e':  chr(0x104b8),
  'ee': chr(0x104df)+macron,
  'ē': chr(0x104df)+macron,
  'ë': '𐓻',
  'eE': chr(0x104df)+macron,
  'g':  chr(0x104f9),
  'h':  chr(0x104e1),
  'hd':  chr(0x104f1),
  'í':  chr(0x104e3) + accent,
  'i':  chr(0x104d9),
  'ii': chr(0x104d9)+macron,
  'ī': chr(0x104d9)+macron,
  'iI': chr(0x104d9)+macron,
  'j':  chr(0x104db),
  'k':  chr(0x104e4),
  'hk': chr(0x104e5),
  'h]': chr(0x104e5),
  'l':  chr(0x104e7),
  'm':  chr(0x104f8),
  'n':  chr(0x104e9),
  'ó':  '𐓪',
  'o': '𐓪',
  'oo': chr(0x104ea)+macron,
  'ō': chr(0x104ea)+macron,
  'oO': chr(0x104ea)+macron,
  'p':  chr(0x104ec),
  'hp': chr(0x104ed),
  's':  chr(0x104ee),
  'sh': chr(0x104ef),
  't':  chr(0x104f5),
  'ht': chr(0x104f1),
  'ts': chr(0x104f2),
  'ts\'': chr(0x104f4),
  'hts': chr(0x104f3),
  'tsh': chr(0x104f4),
  'ú':  chr(0x104f6) + accent,
  'u':  chr(0x104f6),
  'uh': chr(0x104db),
  'uH': chr(0x104db),
  'uH': chr(0x104db),
  'uhd': chr(0x104f6)+chr(0x104f1),
  'uu': chr(0x104f6)+macron,
  'ū': chr(0x104f6)+macron,
  'uU': chr(0x104f6)+macron,
  'v':  chr(0x104ef),
  'w':  chr(0x104f7),
  'x':  chr(0x104f8),
  'y':  chr(0x104e3),
  'yy':  chr(0x104e3)+macron,
  'yY':  chr(0x104e3)+macron,
  'z':  chr(0x104fa),
  'zh': chr(0x104fb),
  # Upper case input.
  'A': chr(0x104b0),
  'Aa': chr(0x104b0)+macron,
  u'\u0100\u0328': chr(0x104b0)+macron,
  'AA': chr(0x104b0)+macron,
  'A\'': chr(0x104b1),
  'Á': chr(0x104b0) + accent,
  'Ā': chr(0x104b0) + macron,
  'B':  chr(0x104b4),
  'Br': chr(0x104b4),
  'BR': chr(0x104b4),
  'Hc':chr(0x104b6),
  'HC':chr(0x104b6),
  'C':  chr(0x104b5),
  'Ch': chr(0x104b6),
  'CH': chr(0x104b6),
  'D':  chr(0x104c8),
  'É':  chr(0x104b7) + accent,
  'E':  chr(0x104b7),
  'Ee': chr(0x104b7)+macron,
  'Ē': chr(0x104b7)+macron,
  'EE': chr(0x104b7)+macron,
  'G':  chr(0x104d1),
  'H':  chr(0x104b9),
  'Hd': chr(0x104f1),
  'HD': chr(0x104c9),
  'H]': chr(0x104c9),
  'HK': chr(0x104c3),
  'Í':  chr(0x104b1) + accent,
  'I':  chr(0x104b1),
  'Ī': chr(0x104b1)+macron,
  'II': chr(0x104b1)+macron,
  'J':  chr(0x104b3),
  'K':  chr(0x104bc),
  'Hk': chr(0x104bd),
  'HK': chr(0x104bd),
  'L':  chr(0x104bf),
  'M':  chr(0x104c0),
  'N':  chr(0x104c1),
  'Ó':  chr(0x104c2) + accent,
  'O':  chr(0x104c2),
  'Ō': chr(0x104c2)+macron,
  'Oo': chr(0x104c2)+macron,
  'OO': chr(0x104c2)+macron,
  'P':  chr(0x104c4),
  'Hp': chr(0x104c5),
  'HP': chr(0x104c5),
  'S':  chr(0x104c6),
  'Sh': chr(0x104c7),
  'SH': chr(0x104c7),
  'T':  chr(0x104cd),
  'Ht': chr(0x104c9),
  'HT': chr(0x104c9),
  'Ts': chr(0x104ca),
  'TS': chr(0x104ca),
  'TS\'': chr(0x104cc),
  'Ts\'': chr(0x104cc),
  'Hts': chr(0x104cb),
  'HTs': chr(0x104cb),
  'HTS': chr(0x104cb),
  'Tsh': chr(0x104cc),
  'TSh': chr(0x104cc),
  'TSH': chr(0x104cc),
  'Ú':  chr(0x104ce) + accent,
  'U':  chr(0x104ce),
  'Uh': chr(0x104b3),
  'UH': chr(0x104b3),
  'Uu': chr(0x104ce)+macron,
  'Ū': chr(0x104ce)+macron,
  'UU': chr(0x104ce)+macron,
  'UHD': chr(0x104ce)+chr(0x104c9),
  'V':  chr(0x104c7),
  'W':  chr(0x104cf),
  'X':  chr(0x104d0),
  'Y':  chr(0x104bb),
  'Yy':  chr(0x104bb)+macron,
  'YY':  chr(0x104bb)+macron,
  'Z':  chr(0x104d2),
  'Zh': chr(0x104d3),
  'ZH': chr(0x104d3),
  ';':  chr(0x104C6) + chr(0x104BC),
  '^':  combiningDotAboveRight,
  ',':  chr(0x104ba),  # HYA character
  u'.': '.',

  # Handle comma and period and other special cases
  ', ':  ', ',
  ',\u000a':  ',\u000a',
  '. ':  '. ',
  '.\u000a': '.\u000a',
  '.\u2008': '.',
  '\u0060': '\u0060',

  '[': chr(0x104d3),
  '{': '{',
  ']': chr(0x104ca),
  'h]': chr(0x104cb),
  'H]': chr(0x104cb),
  '}': '}',
  '/': chr(0x104be),
  '|': chr(0x104c6) + chr(0x104c8),
  '\\': chr(0x104c6) + chr(0x104c8),
  '\"': chr(0x104be),
  # 20-Feb-2017
  # Schwa, etc.
  'Ə': chr(0x104b3),
  'ə': chr(0x104db),
  'Ą': chr(0x104b0) + accent,
  'ą': chr(0x104d8) + accent,
  'Ə̨': chr(0x104b3) + combiningDotAboveRight,
  'ə̨': chr(0x104db) + combiningDotAboveRight,
  'Į': chr(0x104bb) + combiningDotAboveRight,
  'į': chr(0x104e3) + combiningDotAboveRight,
  'Ǫ': chr(0x104c2) + combiningDotAboveRight,
  'ǫ': chr(0x104ea) + combiningDotAboveRight,
  'Ai': chr(0x104b1),
  'ai': chr(0x104d9),
  'Aį': chr(0x104b2),
  'aį': chr(0x104da),
  'Eį': chr(0x104b8),
  'eį': chr(0x104e0),
  'Oį': chr(0x104c3),
  'oį': chr(0x104eb),
  # Accent + cedilla
  u'\ue0b0': chr(0x104b0) + accent + combiningDotAboveRight,
  u'Á\u0328': chr(0x104b0) + accent + combiningDotAboveRight,
  u'\ue0b2': chr(0x104bb) + accent + combiningDotAboveRight,
  u'\u00e1\u0328': chr(0x104bb) + accent + combiningDotAboveRight,
  u'\ue0b1': chr(0x104d8) + accent + combiningDotAboveRight,
  u'\ue0b3': chr(0x104e3) + accent + combiningDotAboveRight,
  # Accent + i + cedilla
  #   Áį áį,   Éį éį,   Óį Óį;   Ái ái
  'Áį': chr(0x104b2) + accent,
  'áį': chr(0x104da) + accent,
  'Éį': chr(0x104b8) + accent,
  'éį': chr(0x104e0) + accent,
  'Óį': chr(0x104c3) + accent,
  'óį': chr(0x104eb) + accent,
  'Ái': chr(0x104b1) + accent,
  'ái': chr(0x104d9) + accent,
  # Accent + macron --> double accent 
  u'\ue070': chr(0x104b0) + doubleAccent,
  u'\ue071': chr(0x104d8) + doubleAccent,
  u'\ue072': chr(0x104b7) + doubleAccent,
  u'\ue073': chr(0x104df) + doubleAccent,
  u'\ue074': chr(0x104bb) + doubleAccent,
  u'\ue075': chr(0x104e3) + doubleAccent,
  u'\ue076': chr(0x104c2) + doubleAccent,
  u'\ue077': chr(0x104ea) + doubleAccent,
  u'\ue078': chr(0x104ce) + doubleAccent,
  u'\ue079': chr(0x104f6) + doubleAccent,
  # Accent + macron + cedilla --> double accent + dot
  u'\ue090': chr(0x104b0) + doubleAccent + combiningDotAboveRight,
  u'\ue091': chr(0x104d8) + doubleAccent + combiningDotAboveRight,
  u'\ue092': chr(0x104bb) + doubleAccent + combiningDotAboveRight,
  u'\ue093': chr(0x104e3) + doubleAccent + combiningDotAboveRight,
  u'\ue094': chr(0x104c2) + doubleAccent + combiningDotAboveRight,
  u'\ue095': chr(0x104ea) + doubleAccent + combiningDotAboveRight,
  # Cedilla combining
  u'\u0328': combiningDotAboveRight,
}

# For parsing input
osage_latin_chars = u"[ÁÍÓ\u00e1\u00ed\u00f3\u0100]\u0328|"  # Vowel followed by ogonek
osage_latin_chars += u"[AÁáEÉéOÓó]į|[ÁAá]i|"  # Vowel + i-ogonek or i.
osage_latin_chars += u"[aeouy]\uf05e|aa|ee|ii|oo|uu|yy|h\]|a\'|ts\'|br|[cs]h|hch|hts|h[cdkpt]|"
osage_latin_chars += u"iu|k\u00d8|k|tsh|t[hs]|zh|\u0060|ó|ì|"

# Comma and period special cases
osage_latin_chars += u", |,\u000a|\. |\.\u000a|\.|\;$"
    
old_osage_chars = u"\uf041\uf041|\uf045\uf045|\uf04f\uf04f|\uf055\uf055|\uf059\uf059|"
old_osage_chars += u"\uf061\uf061|\uf065\uf065|\uf06f\uf06f|" 
old_osage_chars += u"\uf041\uf059|\uf048[\uf043\uf04b\uf050\uf044\uf05d]|"
old_osage_chars += u"[\uf041\uf045\uf04f\uf059][\^\uf05e]|"
old_osage_chars += u"[\\^\uf05e\uf020-\uf0b6]"
# old_osage_chars += u"[\uf020-\uf045\uf048-\uf050\uf053-\uf061\uf065\uf07b-\uf07e\uf0b6]"

combined_chars = old_osage_chars + "|" + osage_latin_chars + "|."
regex2 = re.compile(combined_chars, flags=re.I)


def preParseOldOsage(instring):
    outList = regex2.findall(instring)
    return outList;


def replaceDotSequence(matchobj):
  return '.' * len(matchobj.group(0))


def replaceOsageSyllableDot(matchobj):
  # Omit the dot between two non-space, non-period characters.
  result = matchobj.group(0)[0] + matchobj.group(0)[-1]
  # print('Removing dot from %s giving %s' % (matchobj.group(0).encode('utf-8'),
  #                                          result.encode('utf-8')))
  return result

def oldOsageToUnicode(textIn, convertToLower=True, convertLatin=True,
                      clearOsageDot=True, clearDotSequence=False):
  convertResult = u''

  # Replace sequence of Old Osage dots with periods.
  # TODO: use the flag.
  textIn = re.sub(u'(\uf02e{2,})', replaceDotSequence, textIn)

  textIn = re.sub(u'([^\u0020\uf020\u002e\uf02e][\u002e\uf02e][^\u0020\uf020\u002e\uf02e])', replaceOsageSyllableDot, textIn)

  parsedInput = preParseOldOsage(textIn)
  if debug:
    print('&&&& Text in = >%s<' % textIn)

  if not parsedInput:
    print('!!!! preParse fails')
    return ''

  for index in xrange(len(parsedInput)):
    c = parsedInput[index];

    # Handle ASCII period between two non-white space characters
    #  as if it were an oldOsageDot.
    if c == oldOsageDot and clearOsageDot:
      continue

    out = c
    if c in osage_private_use_map:
      out = osage_private_use_map[c]
    else:
      # It's not in the map.
      if convertLatin:
        if c in osage_latin_to_unicode_map:
          out = osage_latin_to_unicode_map[c]
        else:
          for cc in c:
            print('!!!! Character %s not found (0x%x) in %s' % (
                cc.encode('utf-8'), ord(cc), textIn)
                  )
            convertResult += out

  if convertResult == textIn:
    print('!!! No change in input %s' % (textIn))

  if debug:
    print('&&&& Text out = >%s<' % convertResult)
  return convertResult

def testConvertOld():
  # Debug!
  print('\nOLD OSAGE')
  oldOsageText = u'\uf044\uf041\uf04e\uf059\uf020\uf057\uf041\uf04c\uf059\uf05e'  # u'\'
  expected = u'𐓈𐒰𐓁𐒻 𐓏𐒰𐒿𐒻͘'

  result = oldOsageToUnicode(oldOsageText)

  if result != expected:
    print('Old Osage = %s' % oldOsageText)
    print('** Not converting Old Osage: expected(%d) >%s<. Result(%d) = >%s<' %
           (len(expected), expected, len(result), result))

  print('\nOLD OSAGE Punctuation')
  oldOsagePunctuation = [(u'\uf02d' '-'), (u'\uf020', ' '),
                         (u'\uf05e', '^'), (u'\uf02e', '.')]

  for punct in oldOsagePunctuation:
    result = oldOsageToUnicode(punct[0])
    expected = punct[1]
    if result == expected:
      print('  Punctuation is as expected = %s' % result)
    else:
      print('  Punctuation is *NOT* as expected(%d) = >%s< vs. result(%d) = >%s<' % (
          len(expected), expected, len(result), result))


def testConvertLatin():
  #intext = u"MYY^O^PA WEDOO ^PA AAIIHT UU oouuaa^iiee a\' A'Áįoi ts\' TS\' A\' \uf048"
  intext = u"] [a\' A'ÁįAįáįÉįÓįOįoi ts\' TS\' A\' \uf048"
  expected = u"𐓀𐒻̄͘𐓂͘𐓄𐒰 𐓏𐒷𐓈𐓂̄𐓄𐒰"

  result = oldOsageToUnicode(intext)
  print('TEST      in = %s' % intext)
  print('TEST parsed = %s' %
        [c for c in preParseOldOsage(intext)])
  print('TEST      out = %s' % result)
  print('TEST expected = %s' % expected)
  if result != expected:
    print(' NOT CONVERTED CORRECTLY')
  else:
    print(' Test passes')
  intext2 = u""
  expected = u" !𐓇#$%&'()*+𐒺-𐒾0123456789:𐓆𐒼<=>𐒾@𐒰𐒴𐒵𐓈𐒷𐒹𐒱𐒳𐒼𐒿𐓀𐓁𐓂𐓄𐓆𐓍𐓎𐓇𐓏𐓐𐒻𐓒𐓓𐓆𐓈𐓊͘_`𐒲𐒸𐓃{|}~¶"



def testCommaPeriod():
  print('!!!! testCommanPeriod')
  intext = 'A,B A,'
  expected = u'\ud801\udcb0\ud801\udcba\u0042\u0020\ud801\udcb0\u002c'
  result = oldOsageToUnicode(intext)
  if result != expected:
    print('textCommaPeriod fails on input %s' % intext)

  intext = 'A.B.C A.\u000aD.'
  expected = u'𐒰𐒴C 𐒰.\u000a𐓈.'
  result = oldOsageToUnicode(intext)
  if result != expected:
    print('textCommaPeriod fails on input %s' % intext)


def printResult(expected, result, msg):
  if result != expected:
    print('%s: expected = >%s<, result = >%s<' % 
          (msg,
           expected.encode('utf-8'), result.encode('utf-8')))
  else:
    print('%s: test passes!' % msg)

def testRemoveDots():
  t = u'A. W.a'
  result = oldOsageToUnicode(t)
  expected = u'𐒰. 𐓏𐒲'
  printResult(expected, result, 'testRemoveDots 1')

  t = u'A\uf02ed'
  result = oldOsageToUnicode(t)
  expected = u'𐒰𐓈'
  printResult(expected, result, 'testRemoveDots 2')
  
  t = u'WSX\u002eXYZ'
  result = oldOsageToUnicode(t)
  expected = u'𐓏𐓆𐓐𐓐𐒻𐓒'
  printResult(expected, result, 'testRemoveDots 3')

  t = u'WSX\uf02eXYZ'
  result = oldOsageToUnicode(t)
  # Same expected
  printResult(expected, result, 'testRemoveDots 4')

  t = u'\u002e\u002eJ'
  result = oldOsageToUnicode(t)
  expected = u'..𐒳'
  printResult(expected, result, 'testRemoveDots 5')

  t = u'\u0031\u002e\uf02e'
  result = oldOsageToUnicode(t)
  expected = u'\u0031.'
  printResult(expected, result, 'testRemoveDots 6')

  t = 'HU.HA.;A.'
  result = oldOsageToUnicode(t)
  expected = u'𐒹𐓎𐒹𐒰𐓆𐒼𐒰.'
  printResult(expected, result, 'testRemoveDots 7')

  print( '** testRemoveDots done')


def testCharacterConversions():
  t = '/\\'
  result = oldOsageToUnicode(t)
  expected = u'𐒾𐓆𐓈'
  printResult(expected, result, 'char conversion slash, backslash')

  t = 'QWERTYUIOP{}|ASDFGHJKL:\\"ZXCVBNM<>?'
  result = oldOsageToUnicode(t)
  expected = u'Q𐓏𐒷R𐓍𐒻𐓎𐒱𐓂𐓄{}𐓆𐓈𐒰𐓆𐓈F𐓑𐒹𐒳𐒼𐒿:𐒾𐓒𐓐𐒵𐓇𐒴𐓁𐓀<>?'
  printResult(expected, result, 'Upper case regression test')

  t = 'qwertyuiop[]\asdfghjkl;\'zxcvbnm,./'
  expected = u'q𐓷𐒸r𐓵𐓣𐓶𐓙𐓃𐓬𐓓𐓊𐓆𐓈𐒲𐓮𐓰f𐓹𐓡𐓛𐓤𐓧𐓆𐒼\'𐓺 𐓝𐓯𐓜𐓩𐓸𐒺𐒾'
  result = oldOsageToUnicode(t)
  printResult(expected, result, 'Lower case regression test')

  t = u'\'
  result = oldOsageToUnicode(t)
  expected = u' !𐓇#$%&\'()*+𐒺-𐒾0123456789:𐓆𐒼<=>𐒾@𐒰𐒴𐒵𐓈𐒷𐒹𐒱𐒳𐒼𐒿𐓀𐓁𐓂𐓄𐓆𐓍𐓎𐓇𐓏𐓐𐒻𐓒𐓓𐓆𐓈𐓊͘_`𐒲𐒸𐓃{|}~¶'
  printResult(expected, result, 'All old characters regression test')

  t = 'o  e o a . WEO^O'
  result = oldOsageToUnicode(t)
  print(result)
  expected = u'𐓃  𐒸 𐓃 𐒲 . 𐓏𐒷𐓂͘𐓂'
  printResult(expected, result, 'Lower case vowels eoa')


def main():
  testRemoveDots()

  #Regression test on character conversions.
  testCharacterConversions()

  # Other tests need updating
  testConvertLatin()

  testConvertOld()

  testCommaPeriod()


if __name__ == '__main__':
    main()
