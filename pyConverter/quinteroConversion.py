# -*- coding: utf-8 -*-
#!/usr/bin/env python

import re

# Convert Osage Latin text from Quintero Dictionary to Unicode.

# TIMESTAMP for version information.
TIMESTAMP = "Version 2019-07-03"

# TODO: resolve duplicates in the map.

debug = True  #False

accent = u'\u0301'
doubleAccent = u'\u030B'
macron = u"\u0304"
combiningDotAboveRight = u'\u0358'
osageCaseOffset = 40  # Amount to add to get lower case from upper.
firstOsageUpper = 0x104B0
lastOsageUpper = 0x104D3

minOsageU = chr(firstOsageUpper)
maxOsageU = chr(lastOsageUpper)
lowerCaseOffset = 0x28
oldOsageDot = u'\uf02e'

# Special cases of text that may appear italicized but should not be converted
# to Osage characters
do_not_convert_italics = [
  "LAK", "OM", "OP", "Osage Grammar", "PO", "QU", "WI"
]

grammatical_terms = [
  "1st", "2nd", "3rd", "ADJ", "ADJP", "CUA",
  "(intr.)", "(trans.)",
  # TODO: Add the rest from page xlii.
]

silDoulsQ_to_Unicode_map = {
  u'\u00b0': '\u00f8', # o with bar
  u'\u00b5': '\u00f0', # lowercase eth
  u'\u00bc': 'p\u0323', # p with dot below
  u'\u00be': '\u1eb6', # t with dot below
  u'\u00c3': '\u0194', # capital Latin gamma
  u'\u00c7': '\u0161', # s with caron
  u'\u00cb': '\u017d', # Z with caron
  u'\u00d0': '\u1e33', # k with dot below
  u'\u00d8': '\u02c0', # glottal stop
  u'\u00e0': '\u0105',  # a with ogonek
  u'\u00e2': '\u0105\u0301',  # a acute with ogonek
  u'\u00e3': '\u0263',  # small Latin gamma
  u'\u00e6': '\u207f',  # n superscript
  u'\u00e7': '\u0106',  # s with caron
  u'\u00eb': '\u017e',  # z with caron
  u'\u00ec': '\u02db',  # i with ogonek
  u'\u00f2': '\u01eb',  # o with ogonek
  u'\u00f4': '\u01eb\u0301',  # o acute with ogonek
}

osage_quitero_latin_to_unicode_map = {
  u'\u0020': ' ',
  u'\u0027': '\'',
  u'\u0029': ')',

  u'ã': u'𐓹',
  u'â': u'𐓘͘',  # Plus acute??
  u'à': u'𐓘͘',
  u'á': u'𐓘',
  u'a': u'𐓘',
  u'aa': u'𐓘',
  u'ą̄': u'𐓘͘',
  u'ai': u'𐓙u',
  u'aį': u'𐓚',
  u'ąį': u'𐓚',
  u'æ': u'\u207f',
  u'b': u'𐓬',  # chr(0xd801)+chr(0xdcdc),
  u'br': u'𐓜',
  u'hc': u'𐓲',  #chr(0xd801)+chr(0xdcde),
  u'c':  u'𐓲',  #chr(0xd801)+chr(0xdcdd),
  u'cɂ': u'𐓲’',
  u'č': u'𐓝',
  u'ç': u'𐓮',
  u'Đ': u'𐓍',
  u'ð': u'𐓵',
  u'é': u'𐓟',
  u'd': chr(0x104f0),
  u'e': u'𐓟',
  u'ee': u'𐓟',
  u'ë': u'𐓻',  # Same as 'ž'
  u'ɣ': u'𐓹',
  u'h': u'𐓡',
  u'i': u'𐓣',
  u'ii': u'𐓣',
  u'į': u'𐓣͘',
  u'įį': u'𐓣͘',
  u'î': u'𐓣',
  u'í': u'𐓣',
  u'ì': u'𐓣',
  u'k': u'𐓤',
  u'kk': u'𐓤',
  u'kɂ': u'𐓤’',
  u'k\u00d8': u'𐓤’',
  u'l': u'𐓧',
  u'm': u'𐓨',
  u'n': u'𐓩',
  u'o': u'𐓪',
  u'oo': u'𐓪',
  u'oi': u'𐓫',
  u'oį': u'𐓫',
  u'ô': u'𐓪',
  u'ó': u'𐓪',
  u'ò': u'𐓪',
  u'hp': u'𐓬',
  u'p': u'𐓬',
  u'pɂ': u'𐓬’',
  u's': u'𐓮',
  u'š': u'𐓯',
  u't': u'𐓰',
  u'ht': u'𐓰',
  u'ú': u'𐓰',
  u'u': u'𐓶',
  u'w': u'𐓷',
  u'x': u'𐓸',
  u'z': u'𐓺',
  u'ž': u'𐓻',
  u'ᶕ': u'𐓛͘',
  u'Ø': u'\'',

  # TODO Upper case input.
  u'C': u'𐓊',
  u'D': u'𐓈',
  u'I': u'𐒻',
  u'U': u'𐓎',
  u'T': u'𐓈',

  # Handle comma and period and other special cases
  '!': '!',
  '[': '[',
  ']': ']',
  '_': '_',
  '?': '?',
  '<': '<',
  '>': '>',
  '.': '.',
  ',': ',',
  '(': '(',
  '-': '-',
}
 
# For parsing input
osage_latin_chars = u"[AÁáEÉéOÓóòôžįëìâàA-Za-zčððæɣĐ]"
osage_latin_chars += u"|aa|ee|ii|oo|uu|br|"
osage_latin_chars += u"aį|ąį|hc|cɂ|"

# Comma and period special cases
osage_latin_chars += u"!\(\)\[\]\{\},\.|\;$"

combined_chars = osage_latin_chars + "|."
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

def convertSILDoulousQtoUnicode(intext):
  result_list = []
  for c in intext:
    out = c
    if c in silDoulsQ_to_Unicode_map:
      out = silDoulsQ_to_Unicode_map[c]
    result_list.append(out)
  return ''.join(result_list)

def quiteroOsageToUnicode(textIn, convertToLower=True, convertLatin=True,
                      clearOsageDot=True, clearDotSequence=False):
  convertResult = u''
  notFound = set([])

  # Replace sequence of Old Osage dots with periods.
  # TODO: use the flag.
  textIn = re.sub(u'(\uf02e{2,})', replaceDotSequence, textIn)

  parsedInput = preParseOldOsage(textIn)

  if not parsedInput:
    print('!!!! preParse fails')
    return ''

  for index in range(len(parsedInput)):
    c = parsedInput[index];

    # Handle ASCII period between two non-white space characters
    #  as if it were an oldOsageDot.
    if c == oldOsageDot and clearOsageDot:
      continue

    # It's not in the map.
    if convertLatin:
      if c in osage_quitero_latin_to_unicode_map:
        out = osage_quitero_latin_to_unicode_map[c]
      else:
        for cc in c:
          print('!!!! Character %s not found (0x%x) in %s' % (
              cc.encode('utf-8'), ord(cc), textIn.encode('utf-8')))
        notFound.add(c)
        out = c
      convertResult += out

  # Now look for combinations that need replacement,
  # e.g., a, aa, á, áa -> 𐓘,
  # c, hc, ch=𐓲

  convertResult = re.sub("𐓘𐓘", "𐓘", convertResult)
  convertResult = re.sub("𐓘͘𐓘͘", "𐓘͘", convertResult)
  convertResult = re.sub("𐓟𐓟", "𐓟", convertResult)
  convertResult = re.sub("𐓣𐓣", "𐓣", convertResult)
  convertResult = re.sub("𐓣͘𐓣͘", "𐓣͘", convertResult)
  convertResult = re.sub("𐓪𐓪", "𐓪͘", convertResult)
  convertResult = re.sub("𐓪͘𐓪͘", "𐓪͘͘", convertResult)
  convertResult = re.sub("𐓙𐓙", "𐓙", convertResult)
  convertResult = re.sub("𐓚𐓚", "𐓚", convertResult)
  convertResult = re.sub("𐓫𐓫", "𐓫", convertResult)

  convertResult = re.sub("𐒰𐒰", "𐒰", convertResult)
  convertResult = re.sub("𐒰͘𐒰͘", "𐒰͘", convertResult)
  convertResult = re.sub("𐒷𐒷", "𐒷͘", convertResult)
  convertResult = re.sub("𐒻𐒻", "𐒻", convertResult)
  convertResult = re.sub("𐒻͘𐒻͘", "𐒻͘", convertResult)
  convertResult = re.sub("𐓂͘𐓂͘", "𐓂͘͘", convertResult)
  convertResult = re.sub("𐓂𐓂", "𐓂", convertResult)
  convertResult = re.sub("𐒱𐒱", "𐒱͘", convertResult)
  convertResult = re.sub("𐓃𐓃", "𐓃", convertResult)

  convertResult = re.sub("𐓡𐓲", "𐓲", convertResult)
  convertResult = re.sub("𐓡𐓤", "𐓤͘", convertResult)
  convertResult = re.sub("𐓡𐓬", "𐓬", convertResult)
  convertResult = re.sub("𐒹𐓊", "𐓊", convertResult)
  convertResult = re.sub("𐒹𐒼", "𐒼͘", convertResult)
  convertResult = re.sub("𐒹𐓄", "𐓄", convertResult)
  return convertResult, notFound


def testConvertOld():
  # Debug!
  print('\nOLD OSAGE')
  oldOsageText = u'\uf044\uf041\uf04e\uf059\uf020\uf057\uf041\uf04c\uf059\uf05e'  # u'\'
  expected = u'𐓈𐒰𐓁𐒻 𐓏𐒰𐒿𐒻͘'

  result = oldOsageToUnicode(oldOsageText)

  if result != expected:
    print('Old Osage = %s' % oldOsageText.encode('utf-8'))
    print( '** Not converting Old Osage: expected(%d) >%s<. Result(%d) = >%s<' %
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
  print('TEST      in = %s' % intext.encode("utf-8"))
  print('TEST parsed = %s' %
        [c for c in preParseOldOsage(intext)])
  print('TEST      out = %s' % result.encode("utf-8"))
  print('TEST expected = %s' % expected.encode("utf-8"))
  if result != expected:
    print(' NOT CONVERTED CORRECTLY')
  else:
    print(' Test passes')
  intext2 = u""
  expected = u" !𐓇#$%&'()*+𐒺-𐒾0123456789:𐓆𐒼<=>𐒾@𐒰𐒴𐒵𐓈𐒷𐒹𐒱𐒳𐒼𐒿𐓀𐓁𐓂𐓄𐓆𐓍𐓎𐓇𐓏𐓐𐒻𐓒𐓓𐓆𐓈𐓊͘_`𐒲𐒸𐓃{|}~¶"


def testCommaPeriod():
  print('!!!! testCommanPeriod')
  intext = 'A,B A,'
  expected = u'\U000104b0\U000104ba\u0042\u0020\U000104b0\u002c'
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

  print('** testRemoveDots done')


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
