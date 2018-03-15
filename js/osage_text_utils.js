// Conversion from old font encodings to Osage Unicode.
var osageCaseOffset = 0x28;  // Amount to add to get lower case from upper.
var firstOsageLower = 0x104b0 + osageCaseOffset;
var lastOsageLower = 0x104d8 + osageCaseOffset;

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/charAt#Fixing_charAt()_to_support_non-Basic-Multilingual-Plane_(BMP)_characters

function fixedCharAt(str, idx) {
  var ret = '';
  str += '';
  var end = str.length;

  var surrogatePairs = /[\uD800-\uDBFF][\uDC00-\uDFFF]/g;
  while ((surrogatePairs.exec(str)) != null) {
    var li = surrogatePairs.lastIndex;
    if (li - 2 < idx) {
      idx++;
    } else {
      break;
    }
  }

  if (idx >= end || idx < 0) {
    return '';
  }

  ret += str.charAt(idx);

  if (/[\uD800-\uDBFF]/.test(ret) && /[\uDC00-\uDFFF]/.test(str.charAt(idx + 1))) {
    // Go one further, since one of the "characters" is part of a surrogate pair
    ret += str.charAt(idx + 1);
  }
  return ret;
}

function osageCharToUpper(char) {
  var code = char.codePointAt(0);
  if (char >= firstOsageLower && char <= lastOsageLower) {
    var upperChar = char - osageCaseOffset;
    return String.fromCodePoint(upperChar);
  } else {
    return char;
  }
}

function lowercaseWord(word) {
  var out = word.toLowerCase();
  return out;
}

function uppercaseWord(word, all) {
  // All == false -> only the first character of the selection
  //     == true -> capitalize the entire selection.
  var out = "";
  if (all) {
    // Convert all characters
    out += word.toUpperCase();
  } else {
    // Only the first until after a space or some punctuation.
    var doCap = true;
    var i = 0;
    do {
      var newChar = fixedCharAt(word, i);
      if (newChar) {
	if (doCap) {
	  out += newChar.toUpperCase();
	  doCap = false;
	} else {
	  out += newChar.toLowerCase();
	}
	if (newChar == " " || newChar == "." || newChar == "?" ||
	    newChar == "!" || newChar == "" || newChar == "؟" ||
	    newChar == "⸮") {
	  //Reset to new word.
	  doCap = true;
	}
      }
	i += 1;
      } while (newChar);
  }
  return out;
}
