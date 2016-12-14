# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys

#TODO 13-Dec-2016
# 1. Fix quoted output characters.
# 2. Handle upper and lower case.
# 3. Test

Description = OsageUnicode_description = u'Old Osage font encoding conversion'

# Transliteration from Old Osage to Unicode:
TRANS_LIT_RULES = OLDOSAGE_UNICODE_TRANSLITERATE = u"""# Old Osage to Unicode.
$space = '\u0020';
$macron = \u0304;
$combiningDotAboveRight = \u0358;

\uf020 > $space;
\uf021 > '!',
\uf022 > [\u0x104c7, u104ef],
\uf023 > '#',
\uf024 > '$',
\uf025 > '%',
\uf026 > '&',
\uf027 > "\'",
\uf028 > '(',
\uf029 > ')',
\uf02a > '*',
\uf02b > '+',
\uf02c > [\u104ba, u104e2],
\uf02d > '-',
\uf02e > '.',
\uf02f > [\u104be, u104e6],
\uf030 > '0',
\uf031 > '1',
\uf032 > '2',
\uf033 > '3',
\uf034 > '4',
\uf035 > '5',
\uf036 > '6',
\uf037 > '7',
\uf038 > '8',
\uf039 > '9',
\uf03a >  >',
\uf03b > [' ', ' '],  // Character is no longer used.
\uf03c > '<',
\uf03d > '=',
\uf03e > '>',
\uf03f > [\u104be, u104e6 $,
\uf040 > '@',
\uf041\uf041 > [\u104b0 $macron, \u104d8 $macron],
\uf041 > [\u104b0, u104d8],
\uf041^ > [\u104b0 $combiningDotAboveRight,
     \u104d8 $combiningDotAboveRight],
\uf041\uf05e > [\u104b0 $combiningDotAboveRight,
     \u104d8 $combiningDotAboveRight],\uf042 > [\u104b4, u104dc],
\uf043 > [\u104b5, u104dd],
\uf044 > [\u104c8, u104f0],
\uf045\uf045 > [\u104b7 $macron, \u104df $macron],
\uf045 > [\u104b7, u104df],
\uf045^ > [\u104b7 $combiningDotAboveRight,
     \u104df $combiningDotAboveRight],
\uf045\uf05e > [\u104b7 $combiningDotAboveRight,
     \u104df $combiningDotAboveRight],
\uf048 > [\u104b9, u104e1],
  // The eh-consonants
\uf048\uf043 > [\u104b6, u104de],
\uf048\uf04b > [\u104bd, u104e5],
\uf048\uf050 > [\u104c5, u104ed],
\uf048\uf044 > [\u104c9, u104f1],
\uf048\uf05d > [\u104cb, u104f3],
  
\uf049 > [\u104b1, u104d9],
\uf04a > [\u104b3, u104db],
\uf04b > [\u104bc, u104e4],
\uf04c > [\u104bf, u104e7],
\uf04d > [\u104c0, u104e8],
\uf04e > [\u104c1, u104e9],
\uf04f\uf04f > [\u104c2 $macron, \u104ea $macron],
\uf04f > [\u104c2, u104ea],
\uf04f^ > [\u104c2 $combiningDotAboveRight,
    \u104ea $combiningDotAboveRight],
\uf04f\uf05e > [\u104c2 $combiningDotAboveRight,
    \u104ea $combiningDotAboveRight],
\uf050 > [\u104c4, u104ec],
\uf053 > [\u104c6, u104ee],
\uf054 > [\u104cd, u104f5],
\uf055\uf055 > [\u104ce $macron, \u104f6 $macron],
\uf055 > [\u104ce, u104f6],
\uf055^ > [\u104ce $combiningDotAboveRight,
    \u104f6 $combiningDotAboveRight],
\uf055\uf05e > [\u104ce $combiningDotAboveRight,
    \u104f6 $combiningDotAboveRight],
\uf056 > [\u104c7, u104ef],
\uf057 > [\u104cf, u104f7],
\uf058 > [\u104d0, u104f8],
\uf059\uf059 > [\u104bb $macron, \u104e3 $macron],
\uf059 > [\u104bb, u104e3],
\uf059^ > [\u104bb $combiningDotAboveRight,
    \u104e3 $combiningDotAboveRight],
\uf059\uf05e > [\u104bb $combiningDotAboveRight,
    \u104e3 $combiningDotAboveRight],
\uf05a > [\u104d2, u104fa],  // ??
\uf05b > [\u104d3, u104fb],  // ??
\uf05c > [' ', ' '],  // Character is no longer used.
\uf05d > [\u104ca, u104f2],  // ??],
\uf05e > '^',
\uf05f > '_',
\uf060 > '`',
\uf061 > [\u104b2, u104da],  // ??
\uf065 > [\u104b8, u104e0],  // ??
\uf06f > [\u104c3, u104eb],  // ??
\uf07b > '{',
\uf07c > '|',
\uf07d > '}',
\uf07e > '~',
\uf0b6 > '\u00b6',
"""
  
# Transliteration rules for Latin to Old Osage.
# Transliteration rules for Latin to Unicode.
TRANS_LIT_RULES2 = LATIN_UNICODE_TRANSLITERATE = u"""# Latin to Unicode.
a > [\u104b2), '\uf061'],
aa > [\u104d8 $macron, '\uf041\uf041'], // Macron
a\' > [\u104d9), '\uf049'],
an > [\u104da), '\uf061'],
ah > [\u104db), '\uf04a'],
a^ > [\u104d8 $combiningDotAboveRight, '\uf04a^'],
b >  [\u104dc), '\uf042'],
br > [\u104dc), '\uf042'],
hc > [\u104de), '\uf043'],
c >  [\u104dd), '\uf043'],
ch > [\u104de), '\uf043'],
d >  [\u104f0), '\uf044'],
  // 'e >  [\u104df), '\uf045'],
e >  [\u104b8), '\uf065'],
e^ >  [\u104df $combiningDotAboveRight, '\uf065^'],
ee > [\u104df $macron, '\uf045\uf045'], // Macron
en > [\u104e0), '\uf065'],
g >  [\u104f9), '\uf059'],
h >  [\u104e1), '\uf048'],
hy > [\u104e2), '\uf02c'],
i >  [\u104e3), '\uf059'],
ii > [\u104e3 $macron, '\uf059\uf059'], // Macron
j >  [\u104db), '\uf04a'],
k >  [\u104e4), '\uf04b'],
hk > [\u104e5), '\uf048\uf04b'],
ky > [\u104e6), '\uf048\uf03f'],
l >  [\u104e7), '\uf04c'],
m >  [\u104f8), '\uf04d'],
n >  [\u104e9), '\uf04e'],
  // 'o >  [\u104ea), '\uf04f'],
o > [\u104c3), '\uf06f'],
o^ > [\u104ea $combiningDotAboveRight, '\uf06f^'],
oo > [\u104ea $macron, '\uf04f\uf04f'], // Macron
on > [\u104eb), '\uf06f'],
p >  [\u104ec), '\uf050'],
hp > [\u104ed), '\uf048\uf04b'],
s >  [\u104ee), '\uf053'],
sh > [\u104ef), '\uf022'],
t >  [\u104f5), '\uf054'],
ht > [\u104f1), '\uf048\uf04b'],
ts > [\u104f2), '\uf05d'],
hts > [\u104f3), '\uf054'],
tsh > [\u104f4), '\uf054'],
u >  [\u104f6), '\uf055'],
u^ > [\u104f6 $combiningDotAboveRight, '\uf055^'],
uu > [\u104f6 $macron, '\uf055\uf055'], // Macron
v >  [\u104ef), '\uf056'],
w >  [\u104f7), '\uf057'],
x >  [\u104f8), '\uf058'],
y >  [\u104e3), '\uf05a'],
y^ >  [\u104e3 $combiningDotAboveRight, '\uf05a^'],
z >  [\u104fa), '\uf05a'],
zh > [\u104fb), '\uf05b'],
  // Upper case input.
A > [\u104b0), '\uf041'],
A^ > [\u104b0 $combiningDotAboveRight, '\uf041^'],
Aa > [\u104b0 $macron, '\uf041\uf041'], // Macron
AA > [\u104b0 $macron, '\uf041\uf041'], // Macron
A\' > [\u104b1), '\uf049'],
An > [\u104b2), '\uf061'],
An > [\u104b2), '\uf061'],
AN > [\u104b2), '\uf061'],
Ah > [\u104b3), '\uf04a'],
AH > [\u104b3), '\uf04a'],
B >  [\u104b4), '\uf042'],
Br > [\u104b4), '\uf042'],
BR > [\u104b4), '\uf042'],
Hc >[\u104b6), '\uf043'],
HC >[\u104b6), '\uf043'],
C >  [\u104b5), '\uf043'],
Ch > [\u104b6), '\uf043'],
CH > [\u104b6), '\uf043'],
D >  [\u104c8), '\uf044'],
E >  [\u104b7), '\uf045'],
E^ >  [\u104b7 $combiningDotAboveRight, '\uf045^'],
Ee > [\u104b7 $macron, '\uf045\uf045'], // Macron
EE > [\u104b7 $macron, '\uf045\uf045'], // Macron
En > [\u104b8), '\uf065'],
EN > [\u104b8), '\uf065'],
G >  [\u104d1), '\uf059'],
H >  [\u104b9), '\uf048'],
HY > [\u104ba), '\uf02c'],
I >  [\u104b1), '\uf059'],
//I >  [\u104bb), '\uf059'],
Ii > [\u104bb $macron, '\uf059\uf059'], // Macron
II > [\u104bb $macron, '\uf059\uf059'], // Macron
J >  [\u104b3), '\uf04a'],
K >  [\u104bc), '\uf04b'],
Hk > [\u104bd), '\uf048\uf04b'],
HK > [\u104bd), '\uf048\uf04b'],
Ky > [\u104be), '\uf048\uf03f'],
KY > [\u104be), '\uf048\uf03f'],
L >  [\u104bf), '\uf04c'],
M >  [\u104c0), '\uf04d'],
N >  [\u104c1), '\uf04e'],
O >  [\u104c2), '\uf04f'],
O^ >  [\u104c2 $combiningDotAboveRight, '\uf04f^'],
Oo > [\u104c2 $macron, '\uf04f\uf04f'], // Macron
OO > [\u104c2 $macron, '\uf04f\uf04f'], // Macron
On > [\u104c3), '\uf06f'],
ON > [\u104c3), '\uf06f'],
P >  [\u104c4), '\uf050'],
Hp > [\u104c5), '\uf048\uf04b'],
HP > [\u104c5), '\uf048\uf04b'],
S >  [\u104c6), '\uf053'],
Sh > [\u104c7), '\uf022'],
SH > [\u104c7), '\uf022'],
T >  [\u104cd), '\uf054'],
//T >  [\u104c8), '\uf044'],
Ht > [\u104c9), '\uf048\uf04b'],
HT > [\u104c9), '\uf048\uf04b'],
Ts > [\u104ca), '\uf05d'],
TS > [\u104ca), '\uf05d'],
Hts > [\u104cb), '\uf054'],
HTs > [\u104cb), '\uf054'],
HTS > [\u104cb), '\uf054'],
Tsh > [\u104cc), '\uf054'],
TSh > [\u104cc), '\uf054'],
TSH > [\u104cc), '\uf054'],
U >  [\u104ce), '\uf055'],
U^ >  [\u104ce $combiningDotAboveRight, '\uf055^'],
Uu > [\u104ce $macron, '\uf055\uf055'], // Macron
UU > [\u104ce $macron, '\uf055\uf055'], // Macron
V >  [\u104c7), '\uf056'],
W >  [\u104cf), '\uf057'],
X >  [\u104d0), '\uf058'],
Y >  [\u104bb), '\uf05a'],
Y^ >  [\u104bb $combiningDotAboveRight, '\uf05a^'],
Z >  [\u104d2), '\uf05a'],
Zh > [\u104d3), '\uf05b'],  
ZH > [\u104d3), '\uf05b'],  
; >  [" ", '\uf03b'],
, >  [\u104b9), '\uf02c'],
\[ > [\u104d3), '\uf05b'],
{ > [\u104d3), '\uf05b'],
\] > [\u104cb), '\uf05d'],
} > [\u104cb), '\uf05d'],
\/ > [\u104be), '\uf03f'],
| > [" ", '\uf05c'],
\\ > [" ", '\uf05c'],
\" > [\u104be), '\uf056'],
"""
  
date_entered = '13-Dec-2016'
description = 'First try for transliteration rules for Old Osage to Unicode'

def printRules():
  print 'Rules for %s' % Description
  lines = TRANS_LIT_RULES.split('\n')
  ruleNum = 0
  for line in lines:
    line = line.strip()
    if len(line) > 0 and line[0] != '# ':
      print ('%4d\t%s' % (ruleNum, line))
      ruleNum += 1

def main(argv=None):
  printRules()


if __name__ == "__main__":
    print 'ARGS = %s' % sys.argv 
    sys.exit(main(sys.argv))