# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Tests for Osage conversion to Unicode.

tests = []
tests.append({"""
""",
""" !𐓇#$%&'()*+𐒺-𐒾0123456789: <=>𐒾@𐒰𐒴𐒵𐓈𐒷
𐒹𐒱𐒳𐒼𐒿𐓀𐓁𐓂𐓄𐓆𐓍𐓎𐓇𐓏𐓐𐒻𐓒𐓓 𐓊^_`𐒲𐒸𐓃{|}~¶"""})

tests.append({"""

^^^^^ 
a^e^o^u^y^ A^E^O^U^Y^
aeo""",
"""𐒶𐓉𐒽𐓅𐓋
𐒰̄𐒷̄𐓂̄𐒻̄𐓎̄
𐒰͘𐒷͘𐓂͘𐒻͘𐓎͘ 𐒰͘𐒷͘𐓂͘𐒻͘𐓎͘
𐓘͘𐓟͘𐓪͘𐓶͘𐓣͘ 𐒰͘𐒷͘𐓂͘𐓎͘𐒻͘
𐒲𐒸𐓃"""})

tests.append({"""a aa a' an ah a^ b br hc c ch d e e^ ee en g h hy i ii j k hk ky l
m n o o^ oo on p hp s sh t ht ts hts tsh u u^ uu v w x y y^ z zh
A A^ Aa AA A' An AN Ah AH B Br BR Hc HC C Ch CH D
E E^ Ee EE En EN G H HY I Ii II J K Hk HK Ky KY L M N
O O^ Oo OO On ON P Hp HP S Sh SH T Ht HT Ts TS Hts
HTs HTS Tsh TSh TSH U U^ Uu UU V W X Y Y^ Z Zh ZH
; , [ { ] } / | \ """,
"""𐒲 𐓘̄ 𐓙 𐓚 𐓛 𐓘͘ 𐓜 𐓜 𐓞 𐓝 𐓞 𐓰 𐒸 𐓟͘ 𐓟̄ 𐓠 𐓹 𐓡 𐓢 𐓣 𐓣̄ 𐓛 𐓤 𐓥 𐓦 𐓧
𐓸 𐓩 𐓃 𐓪͘ 𐓪̄ 𐓫 𐓬 𐓭 𐓮 𐓯 𐓵 𐓱 𐓲 𐓳 𐓴 𐓶 𐓶͘ 𐓶̄ 𐓯 𐓷 𐓸 𐓣 𐓣͘ 𐓺 𐓻
𐒰 𐒰͘ 𐒰̄ 𐒰̄ 𐒱 𐒲 𐒲 𐒳 𐒳 𐒴 𐒴 𐒴 𐒶 𐒶 𐒵 𐒶 𐒶 𐓈
𐒷 𐒷͘ 𐒷̄ 𐒷̄ 𐒸 𐒸 𐓑 𐒹 𐒺 𐒱 𐒻̄ 𐒻̄ 𐒳 𐒼 𐒽 𐒽 𐒾 𐒾 𐒿 𐓀 𐓁
𐓂 𐓂͘ 𐓂̄ 𐓂̄ 𐓃 𐓃 𐓄 𐓅 𐓅 𐓆 𐓇 𐓇 𐓍 𐓉 𐓉 𐓊 𐓊 𐓋
𐓋 𐓋 𐓌 𐓌 𐓌 𐓎 𐓎͘ 𐓎̄ 𐓎̄ 𐓇 𐓏 𐓐 𐒻 𐒻͘ 𐓒 𐓓 𐓓
  𐒹 𐓓 𐓓 𐓋 𐓋 𐒾     𐒾 """})
  