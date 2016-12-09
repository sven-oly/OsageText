var macron = "\u0304";
var combiningDotAboveRight = "\u0358";

var osage_private_use_map = {
  '\uf021': '!',
  '\uf022': [String.fromCodePoint(0x104c7), String.fromCodePoint(0x104ef)],
  '\uf023': '#',
  '\uf024': '$',
  '\uf025': '%',
  '\uf026': '&',
  '\uf027': "\'",
  '\uf028': '(',
  '\uf029': ')',
  '\uf02a': '*',
  '\uf02b': '+',
  '\uf02c': [String.fromCodePoint(0x104ba), String.fromCodePoint(0x104de)],
  '\uf02d': '-',
  '\uf02e': '.',
  '\uf02f': [String.fromCodePoint(0x104be), String.fromCodePoint(0x104e6)],
  '\uf030': '0',
  '\uf031': '1',
  '\uf032': '2',
  '\uf033': '3',
  '\uf034': '4',
  '\uf035': '5',
  '\uf036': '6',
  '\uf037': '7',
  '\uf038': '8',
  '\uf039': '9',
  '\uf03a': ':',
  '\uf03b': [' ', ' '],  // Character is no longer used.
  '\uf03c': '<',
  '\uf03d': '=',
  '\uf03e': '>',
  '\uf03f': [String.fromCodePoint(0x104be), String.fromCodePoint(0x104e6)],
  '\uf040': '@',
  '\uf041\uf041': [String.fromCodePoint(0x104b0)+macron, String.fromCodePoint(0x104d8)+macron],
  '\uf041': [String.fromCodePoint(0x104b0), String.fromCodePoint(0x104d8)],
  '\uf042': [String.fromCodePoint(0x104b4), String.fromCodePoint(0x104dc)],
  '\uf043': [String.fromCodePoint(0x104b5), String.fromCodePoint(0x104dd)],
  '\uf044': [String.fromCodePoint(0x104c8), String.fromCodePoint(0x104f0)],
  '\uf045\uf045': [String.fromCodePoint(0x104b7)+macron, String.fromCodePoint(0x104de)+macron],
  '\uf045': [String.fromCodePoint(0x104b7), String.fromCodePoint(0x104de)],
  '\uf048': [String.fromCodePoint(0x104b9), String.fromCodePoint(0x104e1)],
  // The eh-consonants
  '\uf048\uf043': [String.fromCodePoint(0x104b6), String.fromCodePoint(0x104de)],
  '\uf048\uf04b': [String.fromCodePoint(0x104bd), String.fromCodePoint(0x104e5)],
  '\uf048\uf050': [String.fromCodePoint(0x104c5), String.fromCodePoint(0x104ed)],
  '\uf048\uf044': [String.fromCodePoint(0x104c9), String.fromCodePoint(0x104f1)],
  '\uf048\uf05d': [String.fromCodePoint(0x104cb), String.fromCodePoint(0x104f3)],
  
  '\uf049': [String.fromCodePoint(0x104b1), String.fromCodePoint(0x104d9)],
  '\uf04a': [String.fromCodePoint(0x104b3), String.fromCodePoint(0x104db)],
  '\uf04b': [String.fromCodePoint(0x104bc), String.fromCodePoint(0x104e4)],
  '\uf04c': [String.fromCodePoint(0x104bf), String.fromCodePoint(0x104e7)],
  '\uf04d': [String.fromCodePoint(0x104c0), String.fromCodePoint(0x104f8)],
  '\uf04e': [String.fromCodePoint(0x104c1), String.fromCodePoint(0x104e9)],
  '\uf04f\uf04f': [String.fromCodePoint(0x104c2)+macron, String.fromCodePoint(0x104ea)+macron],
  '\uf04f': [String.fromCodePoint(0x104c2), String.fromCodePoint(0x104ea)],
  '\uf050': [String.fromCodePoint(0x104c4), String.fromCodePoint(0x104ec)],
  '\uf053': [String.fromCodePoint(0x104c6), String.fromCodePoint(0x104ee)],
  '\uf054': [String.fromCodePoint(0x104cd), String.fromCodePoint(0x104c6)],
  '\uf055\uf055': [String.fromCodePoint(0x104ce)+macron, String.fromCodePoint(0x104f6)+macron],
  '\uf055': [String.fromCodePoint(0x104ce), String.fromCodePoint(0x104f6)],
  '\uf056': [String.fromCodePoint(0x104c7), String.fromCodePoint(0x104ef)],
  '\uf057': [String.fromCodePoint(0x104cf), String.fromCodePoint(0x104f7)],
  '\uf058': [String.fromCodePoint(0x104d0), String.fromCodePoint(0x104f8)],
  '\uf059\uf059': [String.fromCodePoint(0x104bb)+macron, String.fromCodePoint(0x104e3)+macron],
  '\uf059': [String.fromCodePoint(0x104bb), String.fromCodePoint(0x104e3)],
  '\uf05a': [String.fromCodePoint(0x104d2), String.fromCodePoint(0x104fa)],  // ??
  '\uf05b': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb)],  // ??
  '\uf05c': [' ', ' '],  // Character is no longer used.
  '\uf05d': [String.fromCodePoint(0x104ca), String.fromCodePoint(0x104f2)],  // ??],
  '\uf05e': '^',
  '\uf05f': '_',
  '\uf060': '`',
  '\uf061': [String.fromCodePoint(0x104b2), String.fromCodePoint(0x104da)],  // ??
  '\uf065': [String.fromCodePoint(0x104b8), String.fromCodePoint(0x104e0)],  // ??
  '\uf06f': [String.fromCodePoint(0x104c3), String.fromCodePoint(0x104eb)],  // ??
  '\uf07b': '{',
  '\uf07c': '|',
  '\uf07d': '}',
  '\uf07e': '~',
  '\uf0b6': '\u00b6',
};

// Handles upper case, too.
var osage_latin_to_unicode_map = {
  'a': [String.fromCodePoint(0x104d8), '\uf041'],
  'aa': [String.fromCodePoint(0x104d8)+macron, '\uf041\uf041'], // Macron
  'a\'': [String.fromCodePoint(0x104d9), '\uf049'],
  'an': [String.fromCodePoint(0x104da), '\uf061'],
  'ah': [String.fromCodePoint(0x104db), '\uf04a'],
  'b':  [String.fromCodePoint(0x104dc), '\uf042'],
  'br': [String.fromCodePoint(0x104dc), '\uf042'],
  'hch':[String.fromCodePoint(0x104dd), '\uf043'],
  'c':  [String.fromCodePoint(0x104de), '\uf043'],
  'ch': [String.fromCodePoint(0x104de), '\uf043'],
  'd':  [String.fromCodePoint(0x104f0), '\uf044'],
  'e':  [String.fromCodePoint(0x104b7), '\uf045'],
  'ee': [String.fromCodePoint(0x104de)+macron, '\uf045\uf045'], // Macron
  'en': [String.fromCodePoint(0x104e0), '\uf065'],
  'g':  [String.fromCodePoint(0x104f9), '\uf059'],
  'h':  [String.fromCodePoint(0x104e1), '\uf048'],
  'hy': [String.fromCodePoint(0x104e2), '\uf02c'],
  'i':  [String.fromCodePoint(0x104e3), '\uf059'],
  'ii': [String.fromCodePoint(0x104e3)+macron, '\uf059\uf059'], // Macron
  'j':  [String.fromCodePoint(0x104db), '\uf04a'],
  'k':  [String.fromCodePoint(0x104e4), '\uf04b'],
  'hk': [String.fromCodePoint(0x104e5), '\uf048\uf04b'],
  'ky': [String.fromCodePoint(0x104e6), '\uf048\uf03f'],
  'l':  [String.fromCodePoint(0x104e7), '\uf04c'],
  'm':  [String.fromCodePoint(0x104f8), '\uf04d'],
  'n':  [String.fromCodePoint(0x104e9), '\uf04e'],
  'o':  [String.fromCodePoint(0x104ea), '\uf04f'],
  'oo': [String.fromCodePoint(0x104ea)+macron, '\uf04f\uf04f'], // Macron
  'on': [String.fromCodePoint(0x104eb), '\uf06f'],
  'p':  [String.fromCodePoint(0x104ec), '\uf050'],
  'hp': [String.fromCodePoint(0x104ed), '\uf048\uf04b'],
  's':  [String.fromCodePoint(0x104ee), '\uf053'],
  'sh': [String.fromCodePoint(0x104ef), '\uf022'],
  't':  [String.fromCodePoint(0x104f0), '\uf044'],
  'ht': [String.fromCodePoint(0x104f1), '\uf048\uf04b'],
  'ts': [String.fromCodePoint(0x104f2), '\uf05d'],
  'hts': [String.fromCodePoint(0x104f3), '\uf054'],
  'tsh': [String.fromCodePoint(0x104f4), '\uf054'],
  'u':  [String.fromCodePoint(0x104f6), '\uf055'],
  'uu': [String.fromCodePoint(0x104f6)+macron, '\uf055\uf055'], // Macron
  'v':  [String.fromCodePoint(0x104ef), '\uf056'],
  'w':  [String.fromCodePoint(0x104f7), '\uf057'],
  'x':  [String.fromCodePoint(0x104f8), '\uf058'],
  'y':  [String.fromCodePoint(0x104e3), '\uf05a'],
  'z':  [String.fromCodePoint(0x104fa), '\uf05a'],
  'zh': [String.fromCodePoint(0x104fb), '\uf05b'],
  // Upper case input.
  'A': [String.fromCodePoint(0x104b0), '\uf041'],
  'Aa': [String.fromCodePoint(0x104b0)+macron, '\uf041\uf041'], // Macron
  'AA': [String.fromCodePoint(0x104b0)+macron, '\uf041\uf041'], // Macron
  'A\'': [String.fromCodePoint(0x104b1), '\uf049'],
  'An': [String.fromCodePoint(0x104b2), '\uf061'],
  'An': [String.fromCodePoint(0x104b2), '\uf061'],
  'Ah': [String.fromCodePoint(0x104b3), '\uf04a'],
  'Ah': [String.fromCodePoint(0x104b3), '\uf04a'],
  'B':  [String.fromCodePoint(0x104b4), '\uf042'],
  'Br': [String.fromCodePoint(0x104b4), '\uf042'],
  'BR': [String.fromCodePoint(0x104b4), '\uf042'],
  'hch':[String.fromCodePoint(0x104b5), '\uf043'],
  'Hch':[String.fromCodePoint(0x104b5), '\uf043'],
  'HCh':[String.fromCodePoint(0x104b5), '\uf043'],
  'HCH':[String.fromCodePoint(0x104b5), '\uf043'],
  'c':  [String.fromCodePoint(0x104b6), '\uf043'],
  'C':  [String.fromCodePoint(0x104b6), '\uf043'],
  'ch': [String.fromCodePoint(0x104b6), '\uf043'],
  'Ch': [String.fromCodePoint(0x104b6), '\uf043'],
  'CH': [String.fromCodePoint(0x104b6), '\uf043'],
  'D':  [String.fromCodePoint(0x104c8), '\uf044'],
  'E':  [String.fromCodePoint(0x104b7), '\uf045'],
  'Ee': [String.fromCodePoint(0x104b7)+macron, '\uf045\uf045'], // Macron
  'EE': [String.fromCodePoint(0x104b7)+macron, '\uf045\uf045'], // Macron
  'En': [String.fromCodePoint(0x104b8), '\uf065'],
  'EN': [String.fromCodePoint(0x104b8), '\uf065'],
  'G':  [String.fromCodePoint(0x104d1), '\uf059'],
  'H':  [String.fromCodePoint(0x104b9), '\uf048'],
  'HY': [String.fromCodePoint(0x104ba), '\uf02c'],
  'I':  [String.fromCodePoint(0x104bb), '\uf059'],
  'Ii': [String.fromCodePoint(0x104bb)+macron, '\uf059\uf059'], // Macron
  'II': [String.fromCodePoint(0x104bb)+macron, '\uf059\uf059'], // Macron
  'J':  [String.fromCodePoint(0x104b3), '\uf04a'],
  'K':  [String.fromCodePoint(0x104bc), '\uf04b'],
  'Hk': [String.fromCodePoint(0x104bd), '\uf048\uf04b'],
  'HK': [String.fromCodePoint(0x104bd), '\uf048\uf04b'],
  'Ky': [String.fromCodePoint(0x104be), '\uf048\uf03f'],
  'KY': [String.fromCodePoint(0x104be), '\uf048\uf03f'],
  'L':  [String.fromCodePoint(0x104bf), '\uf04c'],
  'M':  [String.fromCodePoint(0x104c0), '\uf04d'],
  'N':  [String.fromCodePoint(0x104c1), '\uf04e'],
  'O':  [String.fromCodePoint(0x104c2), '\uf04f'],
  'Oo': [String.fromCodePoint(0x104c2)+macron, '\uf04f\uf04f'], // Macron
  'OO': [String.fromCodePoint(0x104c2)+macron, '\uf04f\uf04f'], // Macron
  'On': [String.fromCodePoint(0x104c3), '\uf06f'],
  'ON': [String.fromCodePoint(0x104c3), '\uf06f'],
  'P':  [String.fromCodePoint(0x104c4), '\uf050'],
  'Hp': [String.fromCodePoint(0x104c5), '\uf048\uf04b'],
  'HP': [String.fromCodePoint(0x104c5), '\uf048\uf04b'],
  'S':  [String.fromCodePoint(0x104c6), '\uf053'],
  'Sh': [String.fromCodePoint(0x104c7), '\uf022'],
  'SH': [String.fromCodePoint(0x104c7), '\uf022'],
  'T':  [String.fromCodePoint(0x104c8), '\uf044'],
  'Ht': [String.fromCodePoint(0x104c9), '\uf048\uf04b'],
  'HT': [String.fromCodePoint(0x104c9), '\uf048\uf04b'],
  'Ts': [String.fromCodePoint(0x104ca), '\uf05d'],
  'TS': [String.fromCodePoint(0x104ca), '\uf05d'],
  'Hts': [String.fromCodePoint(0x104cb), '\uf054'],
  'HTs': [String.fromCodePoint(0x104cb), '\uf054'],
  'HTS': [String.fromCodePoint(0x104cb), '\uf054'],
  'Tsh': [String.fromCodePoint(0x104cc), '\uf054'],
  'TSh': [String.fromCodePoint(0x104cc), '\uf054'],
  'TSH': [String.fromCodePoint(0x104cc), '\uf054'],
  'U':  [String.fromCodePoint(0x104ce), '\uf055'],
  'Uu': [String.fromCodePoint(0x104ce)+macron, '\uf055\uf055'], // Macron
  'UU': [String.fromCodePoint(0x104ce)+macron, '\uf055\uf055'], // Macron
  'V':  [String.fromCodePoint(0x104c7), '\uf056'],
  'W':  [String.fromCodePoint(0x104cf), '\uf057'],
  'X':  [String.fromCodePoint(0x104d0), '\uf058'],
  'Y':  [String.fromCodePoint(0x104bb), '\uf05a'],
  'Z':  [String.fromCodePoint(0x104d2), '\uf05a'],
  'Zh': [String.fromCodePoint(0x104d3), '\uf05b'],  
  'ZH': [String.fromCodePoint(0x104d3), '\uf05b'],  
  '\;':  [" ", " ", '\uf03b'],
  '\[':  [String.fromCodePoint(0x104d3), '\uf05b'],
  '\]':  [String.fromCodePoint(0x104dcb), '\uf05d'],
  '\/': [String.fromCodePoint(0x104dbe), '\uf03f'],
  '\\': [" ", " ", '\uf05c'],
  // TODO: Finish these.
}

var minOsageU = String.fromCodePoint(0x104b0);
var maxOsageU = String.fromCodePoint(0x104d8);
var lowerCaseOffset = 0x28;

// Converts from old Osage codepoints to Unicode Standard.
// Converts to lower case if the flag is set.
// TODO: Convert to UTF-16.
function oldOsageToUnicode(textIn, convertToLower) {
  var convertResult = "";
  var index;
  var outputIsUTF16 = true;

  var parsedInput = preParseOldOsage(textIn);
  if (!parsedInput) {
    return "";
  }
  for (index = 0; index < parsedInput.length; index ++) {
    var c = parsedInput[index];
    var result = osage_private_use_map[c];
    if (result) {
      if (Array.isArray(result)) {
        if (convertToLower) {
          out = result[1];  // The lower case.
        } else {
          out = result[0];  // Upper case.
        }
      } else {
        out = result;  // Only a single character.
      }
    } else {
      // It's not in the map.
      out = c;
    }
    convertResult += out;
  }
  if (outputIsUTF16) {
    var convertResultUTF16 = "";
    var u16list = [];
    for (var i = 0; i < convertResult.length; i++) {
      var cp = convertResult.codePointAt(i);
      var utf16Result = getUnicodeCharacter(cp);
      if (typeof utf16Result === 'string') {
        var len16 = utf16Result.length;
          for (var j = 0; j < len16; j ++) {
            var charCode = utf16Result.codePointAt(j);
          }
      }
      u16list.push(utf16Result);
    }
    return u16list.join("");
  } else {
    return convertResult;
  }
}

// Converts from old Osage codepoints to Unicode Standard.
// Converts to lower case if the flag is set.
// TODO: Convert to UTF-16.
function latinToUnicode(textIn, convertToLower) {
  var convertResult = "";
  var index;
  var outputIsUTF16 = true;

  var parsedInput = preParseLatin(textIn);
  for (index = 0; index < parsedInput.length; index ++) {
    var c = parsedInput[index];
    if (convertToLower) {
      c = c.toLowerCase();
    }
    var result = osage_latin_to_unicode_map[c];
    if (result) {
      if (Array.isArray(result)) {
        out = result[0];  // Upper case.
      } else {
        out = result;  // Only a single character.
      }
    } else {
      // It's not in the map.
      out = c;
    }
    convertResult += out;
  }
  if (outputIsUTF16) {
    var convertResultUTF16 = "";
    var u16list = [];
    for (var i = 0; i < convertResult.length; i++) {
      var cp = convertResult.codePointAt(i);
      var utf16Result = getUnicodeCharacter(cp);
      if (typeof utf16Result === 'string') {
        var len16 = utf16Result.length;
          for (var j = 0; j < len16; j ++) {
            var charCode = utf16Result.codePointAt(j);
          }
      }
      u16list.push(utf16Result);
    }
    return u16list.join("");
  } else {
    return convertResult;
  }
}

// Converts from old Osage codepoints to Unicode Standard.
// Converts to lower case if the flag is set.
// TODO: Convert to UTF-16.
function latinToOldOsage(textIn, convertToLower) {
  var convertResult = "";
  var index;
  var outputIsUTF16 = true;
  var out;

  var parsedInput = preParseLatin(textIn);
  if (!parsedInput) {
    return "";
  }

  for (index = 0; index < parsedInput.length; index ++) {
    var c = parsedInput[index].toLowerCase();
    var result = osage_latin_to_unicode_map[c];
    if (result) {
      if (Array.isArray(result)) {
          out = result[1];
      } else {
        out = result;  // Only a single character.
      }
    } else {
      // It's not in the map.
      out = c;
    }
    convertResult += out;
  }
  if (outputIsUTF16) {
    var convertResultUTF16 = "";
    var u16list = [];
    for (var i = 0; i < convertResult.length; i++) {
      var cp = convertResult.codePointAt(i);
      var utf16Result = getUnicodeCharacter(cp);
      if (typeof utf16Result === 'string') {
        var len16 = utf16Result.length;
          for (var j = 0; j < len16; j ++) {
            var charCode = utf16Result.codePointAt(j);
          }
      }
      u16list.push(utf16Result);
    }
    return u16list.join("");
  } else {
    return convertResult;
  }
}

var osage_latin_regex = /aa|a\'|ah|an|a|br|b|ch|c|d|ee|en|e|g|hch|hk|hp|hts|ht|hy|h|ii|iu|i|j|ky|k|l|m|n|on|oo|o|p|sh|s|tt|th|tsh|ts|ts\'|t|uu|u|v|w|x|y|zh|z|\'|\[|\]|\\|\/|6|\;|\S|\s/gi;

var combiningDotUpAboveRight = "\u0358";

// Use regular expression to greedily process input string, producing list of strings
// to be converted. E.g., 'htathanh' should give {"ht", "a", "th", "n", "h"}
function preParseLatin(instring) {
  outList = instring.match(osage_latin_regex);
  return outList;
}

// For converting input to sets of connected characters.
var old_osage_regex = /\uf021|\uf022|\uf023|\uf024|\uf025|\uf026|\uf027|\uf028|\uf029|\uf02a|\uf02b|\uf02c|\uf02d|\uf02e|\uf02f|\uf030|\uf031|\uf032|\uf033|\uf034|\uf035|\uf036|\uf037|\uf038|\uf039|\uf03a|\uf03b|\uf03c|\uf03d|\uf03e|\uf03f|\uf040|\uf041\uf041|\uf041|\uf042|\uf043|\uf044|\uf045\uf045|\uf045|\uf048\uf043|\uf048\uf04b|\uf048\uf050|\uf048\uf044|\uf048\uf05d|\uf048|\uf049|\uf04a|\uf04b|\uf04c|\uf04d|\uf04e|\uf04f\uf04f|\uf04f|\uf050|\uf053|\uf054|\uf055\uf055|\uf055|\uf056|\uf057|\uf058|\uf059\uf059|\uf059|\uf05a|\uf05b|\uf05c|\uf05d|\uf05e|\uf05f|\uf060|\uf061|\uf065|\uf06f|\uf07b|\uf07c|\uf07d|\uf07e|\uf0b6|\S|\s/gi;

function preParseOldOsage(instring) {
  var outList = instring.match(old_osage_regex);
  return outList;
}
