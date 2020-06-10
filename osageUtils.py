# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import print_function
from builtins import chr
import sys

# Utilities to convert Osage text.
osageUpperFirst = 0x104B0
osageUpperLast = 0x104D3

osageLowerFirst = 0x104D8
osageLowerLast = 0x104DFB

LOWEROFFSET = osageLowerFirst - osageUpperFirst


# Convert to lower case
def toLower(word):
  lower_out = u''
  for char in word:
    out_num = ord(char)
    if out_num >= osageUpperFirst and out_num <= osageUpperLast:
      out_num = out_num + LOWEROFFSET
    print('toLower %s -> %s (%x)' % (char, chr(out_num), out_num))
    lower_out += chr(out_num)
  return lower_out


def toUpper(word):
  upper_out = u''
  for char in word:
    out_num = ord(char)
    if out_num >= osageLowerFirst and out_num <= osageLowerLast:
      out_num = out_num - LOWEROFFSET
    print('toUpper %s -> %s (%x)' % (char, chr(out_num), out_num))
    upper_out += chr(out_num)

  return upper_out


def main(argv=None):
  u = u'𐒰𐒱𐒲𐒳𐒴𐒵𐒶𐒷𐒸𐒹𐒺𐒻𐒼𐒽𐒾𐒿𐓀𐓁𐓂𐓃𐓄𐓅𐓆𐓇𐓈𐓉𐓊𐓋𐓌𐓍𐓎𐓏𐓐𐓑𐓒𐓓'
  lower = u'𐓘𐓙𐓚𐓛𐓜𐓝𐓞𐓟𐓠𐓡𐓢𐓣𐓤𐓥𐓦𐓧𐓨𐓩𐓪𐓫𐓬𐓭𐓮𐓯𐓰𐓱𐓲𐓳𐓴𐓵𐓶𐓷𐓸𐓹𐓺𐓻'
  lowered = toLower(u)
  print('Lower = %s' % lowered)
  print('Upper = %s' % toUpper(lower))


if __name__ == "__main__":
    print('ARGS = %s' % sys.argv)
    sys.exit(main(sys.argv))