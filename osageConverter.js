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
  '\uf03b': ['', ''],  // Character is no longer used.
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
  '\uf05c': ['', ''],  // Character is no longer used.
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

var osage_latin_regex = "aa|an|a\'|a|br|ch|ç|ee|en|e|hk|h|i|ii|iu|k|l|m|n|oo|o|on|p|p\'|s|sh|sk|ts|ts'|t|th|uu|u|w|x|z|zh";

var osage_latin_to_unicode_map = {
  //'\uf02f': [String.fromCodePoint(0x104be), String.fromCodePoint(0x104e6), '\uf02f'], // ??
  // '\uf03f': [String.fromCodePoint(0x104be), String.fromCodePoint(0x104e6), '\uf03f'], // ?
  'a': [String.fromCodePoint(0x104b0), String.fromCodePoint(0x104d8), '\uf041'],
  'aa': [String.fromCodePoint(0x104b0)+macron, String.fromCodePoint(0x104d8)+macron, '\uf041\uf041'], // Macron
  'an': [String.fromCodePoint(0x104b2), String.fromCodePoint(0x104da), '\uf061'],
  'a\'': [String.fromCodePoint(0x104b1), String.fromCodePoint(0x104d9), '\uf049'],
  'b':  [String.fromCodePoint(0x104b4), String.fromCodePoint(0x104dc), '\uf042'],
  'br': [String.fromCodePoint(0x104b4), String.fromCodePoint(0x104dc), '\uf043'],
  'c': [String.fromCodePoint(0x104b5), String.fromCodePoint(0x104dd),'\uf043'],
  'ch': [String.fromCodePoint(0x104b5), String.fromCodePoint(0x104dd),'\uf043'],
  'e':  [String.fromCodePoint(0x104b7), String.fromCodePoint(0x104de), '\uf045'],
  'd':  [String.fromCodePoint(0x104c8), String.fromCodePoint(0x104f0), '\uf044'],
  'ee': [String.fromCodePoint(0x104b7)+macron, String.fromCodePoint(0x104de)+macron, '\uf045\uf045'], // Macron
  'en': [String.fromCodePoint(0x104b8), String.fromCodePoint(0x104e0), '\uf065'],
  'h': [String.fromCodePoint(0x104b9), String.fromCodePoint(0x104e1), '\uf048'],
  'hk': [String.fromCodePoint(0x104bd), String.fromCodePoint(0x104e5), '\uf048\uf04b'],
  // '\uf04a': [String.fromCodePoint(0x104b3), String.fromCodePoint(0x104db), '\uf04a'],
  'i': [String.fromCodePoint(0x104bb), String.fromCodePoint(0x104e3), '\uf059'],
  'ii': [String.fromCodePoint(0x104bb)+macron, String.fromCodePoint(0x104e3)+macron, '\uf059\uf059'], // Macron
  'iu': [String.fromCodePoint(0x104ce), String.fromCodePoint(0x104f6), '\uf055'],
  'k': [String.fromCodePoint(0x104bc), String.fromCodePoint(0x104e4), '\uf04b'],
  'k\'': [String.fromCodePoint(0x104bc), String.fromCodePoint(0x104e4), '\uf04b'],
  'l': [String.fromCodePoint(0x104bf), String.fromCodePoint(0x104e7), '\uf04c'],
  'm': [String.fromCodePoint(0x104c0), String.fromCodePoint(0x104f8), '\uf04d'],
  'n': [String.fromCodePoint(0x104c1), String.fromCodePoint(0x104e9), '\uf04e'],
  'o': [String.fromCodePoint(0x104c2), String.fromCodePoint(0x104ea), '\uf04f'],
  'oo': [String.fromCodePoint(0x104c2)+macron, String.fromCodePoint(0x104ea)+macron, '\uf04f\uf04f'], // Macron
  'on': [String.fromCodePoint(0x104c3), String.fromCodePoint(0x104eb), '\uf06f'],
  'p': [String.fromCodePoint(0x104c4), String.fromCodePoint(0x104ec), '\uf050'],
  'pp': [String.fromCodePoint(0x104c4), String.fromCodePoint(0x104ec), '\uf050'],
  'p\'': [String.fromCodePoint(0x104c4), String.fromCodePoint(0x104ec), '\uf050'],
  's': [String.fromCodePoint(0x104c6), String.fromCodePoint(0x104ee), '\uf053'],
  'sh': [String.fromCodePoint(0x104c7), String.fromCodePoint(0x104ef), '\uf022'],
  'sk': ['', '', '\uf03b'],
  'st': ['', '', '\uf05c'],
  't': [String.fromCodePoint(0x104c8), String.fromCodePoint(0x104f0), '\uf044'],
  'tt': [String.fromCodePoint(0x104c8), String.fromCodePoint(0x104f0), '\uf044'],
  'ts': [String.fromCodePoint(0x104ca), String.fromCodePoint(0x104f2), '\uf05d'],
  'ts\'': [String.fromCodePoint(0x104ca), String.fromCodePoint(0x104f2), '\uf05d'],
  'th': [String.fromCodePoint(0x104cd), String.fromCodePoint(0x104c6), '\uf054'],
  'u': [String.fromCodePoint(0x104ce), String.fromCodePoint(0x104f6), '\uf055'],
  'uu': [String.fromCodePoint(0x104ce)+macron, String.fromCodePoint(0x104f6)+macron, '\uf055\uf055'], // Macron
  'v': [String.fromCodePoint(0x104c7), String.fromCodePoint(0x104ef), '\uf05'],
  'w': [String.fromCodePoint(0x104cf), String.fromCodePoint(0x104f7), '\uf057'],
  'x': [String.fromCodePoint(0x104d0), String.fromCodePoint(0x104f8), '\uf058'],
  // '\uf05c': ['', '', '\uf05c'],
  'z': [String.fromCodePoint(0x104d2), String.fromCodePoint(0x104fa), '\uf05a'],
  'zh': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb), '\uf05b'],
  '\'': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb), '\uf060'],
  // TODO: Finish these.
  '^': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb), '\uf06f'],
  '[': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb), '\uf06f'],
  ']': [String.fromCodePoint(0x104d3), String.fromCodePoint(0x104fb), '\uf06f'],
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
    var c = parsedInput[index].toLowerCase();
    var result = osage_latin_to_unicode_map[c];
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
function latinToOldOsage(textIn, convertToLower) {
  var convertResult = "";
  var index;
  var outputIsUTF16 = true;

  var parseInput = preParseLatin(textIn);

  //for (index = 0; index < textIn.length; index ++) {
  for (index = 0; index < parseInput.length; index ++) {
    var c = parseInput[index].toLowerCase();
    var result = osage_latin_to_unicode_map[c];
    if (result) {
      if (Array.isArray(result)) {
          out = result[2];
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

var osage_latin_regex = /aa|an|a\'|a|br|b|ch|d|ee|en|e|hk|h|ii|iu|i|k'|k|l|m|n|on|oo|o|p\'|pp|p|sh|sk|st|s|ts|ts'|tt|th|t|uu|u|v|w|x|y|zh|z|\'|\s/gi;

var combiningDotUpAboveRight = "\u0358";

// Use regular expression to greedily process input string, producing list of strings
// to be converted. E.g., 'ttathanh' should give {"tt", "a", "th", "n", "h"}
function preParseLatin(instring) {
  outList = instring.match(osage_latin_regex);
  return outList;
}

// For converting input to sets of connected characters.
var old_osage_regex = /\uf021|\uf022|\uf023|\uf024|\uf025|\uf026|\uf027|\uf028|\uf029|\uf02a|\uf02b|\uf02c|\uf02d|\uf02e|\uf02f|\uf030|\uf031|\uf032|\uf033|\uf034|\uf035|\uf036|\uf037|\uf038|\uf039|\uf03a|\uf03b|\uf03c|\uf03d|\uf03e|\uf03f|\uf040|\uf041\uf041|\uf041|\uf042|\uf043|\uf044|\uf045\uf045|\uf045|\uf048|\uf049|\uf04a|\uf04b|\uf04c|\uf04d|\uf04e|\uf04f\uf04f|\uf04f|\uf050|\uf053|\uf054|\uf055\uf055|\uf055|\uf056|\uf057|\uf058|\uf059\uf059|\uf059|\uf05a|\uf05b|\uf05c|\uf05d|\uf05e|\uf05f|\uf060|\uf061|\uf065|\uf06f|\uf07b|\uf07c|\uf07d|\uf07e|\uf0b6|\s/gi;

function preParseOldOsage(instring) {
  outList = instring.match(old_osage_regex);
  return outList;
}
