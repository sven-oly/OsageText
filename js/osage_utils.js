// Fills the input with all the characters in the new Unicode Osage range.
var unicodeVowels = [0x104b0, 0x104b7, 0x104bb, 0x104c2, 0x104ce,
  0x104d8, 0x104df, 0x104e3, 0x104ea, 0x104f6];
var unicodeVowelSubset = [0x104b0, 0x104bb, 0x104c2,
  0x104d8, 0x104e3, 0x104ea];

  // Fills the input with all the characters in the old Osage range.
  function fillWithOldOsage(target, hex_target) {
    var output_text = document.getElementById(target);
    var outputString = "";
    var codePt;
    for (codePt = 0xf020; codePt < 0xf046; codePt++) {
      outputString += String.fromCodePoint(codePt);
    }
    outputString += String.fromCodePoint(0x000a);

    for (codePt = 0xf048; codePt < 0xf051; codePt++) {
      outputString += String.fromCodePoint(codePt);
    }
    for (codePt = 0xf053; codePt < 0xf062; codePt++) {
      outputString += String.fromCodePoint(codePt);
    }
    outputString += String.fromCodePoint(0xf065);
    outputString += String.fromCodePoint(0xf06f);
    outputString += String.fromCodePoint(0xf07b);
    outputString += String.fromCodePoint(0xf07c);
    outputString += String.fromCodePoint(0xf07d);
    outputString += String.fromCodePoint(0xf07e);
    outputString += String.fromCodePoint(0xf0b6);

    output_text.innerHTML = outputString;
    output_text.value = outputString;

    updateHex(target, hex_target);
  }

function fillWithUnicodeOsage(target, hex_target) {
  var output_text = document.getElementById(target);
  var outputString = "";
  for (var codePt = 0x104b0; codePt <= 0x104d3; codePt++) {
    outputString += getUnicodeCharacter(codePt);
  }
  outputString += "\n";
  for (var codePt = 0x104d8; codePt <= 0x104fb; codePt++) {
    outputString += getUnicodeCharacter(codePt);
  }
  output_text.innerHTML = outputString;
  output_text.value = outputString;

  if (hex_target) {
    updateHex(target, hex_target);
  }
}

// Special cases.
function fillOsageCombos(target, hex_target) {
  var output_text = document.getElementById(target);
  outputString = "\n ^ ^ \n^^^^^ " +
    "" + 
    "\na^e^o^u^y^ A^E^O^U^Y^\naeo";
  output_text.innerHTML = outputString;
  output_text.value = outputString;
  if (hex_target) {
    updateHex(target, hex_target);
  }
}

function fillWithUnicodeOsageMacron(target, hex_target) {
  var output_text = document.getElementById(target);
  var outputString = "";
  var macron = "\u0304";
  for (var codePt in unicodeVowels) {
    outputString += getUnicodeCharacter(codePt);
    outputString += macron;
  }
  outputString += "\n";
  for (var codePt = 0x104d8; codePt <= 0x104fb; codePt++) {
    outputString += getUnicodeCharacter(codePt);
    outputString += macron;
  }
  output_text.innerHTML = outputString;
  output_text.value = outputString;

  updateHex(target, hex_target);
}

function fillWithUnicodeOsageDotted(target, hex_target) {
  var combiningDotAboveRight = "\u0358";
  var output_text = document.getElementById(target);
  var outputString = "";
  for (var codePt = 0x104b0; codePt <= 0x104d3; codePt++) {
    outputString += getUnicodeCharacter(codePt);
    outputString += combiningDotAboveRight;
  }
  outputString += "\n";
  for (var codePt = 0x104d8; codePt <= 0x104fb; codePt++) {
    outputString += getUnicodeCharacter(codePt);
    outputString += combiningDotAboveRight;
  }
  output_text.innerHTML = outputString;
  output_text.value = outputString;

  updateHex(target, hex_target);
}

function fillWithUnicodeOsageStringAppended(target, stringToAppend, hex_target) {
  var output_text = document.getElementById(target);
  var outputString = "";
  for (var index in unicodeVowels) {
  //for (var codePt = 0x104b0; codePt <= 0x104d3; codePt++) {
    outputString += getUnicodeCharacter(unicodeVowels[index]); //getUnicodeCharacter(codePt);
    outputString += stringToAppend;
  }
/*  outputString += "\n";
  for (var codePt = 0x104d8; codePt <= 0x104fb; codePt++) {
    outputString += getUnicodeCharacter(codePt);
    outputString += stringToAppend;
  }
  */
  output_text.innerHTML = outputString;
  output_text.value = outputString;

  updateHex(target, hex_target);
}

function fillWithUnicodeOsageVowelSubsetAppended(target, stringToAppend, hex_target) {
  var output_text = document.getElementById(target);
  var outputString = "";
  for (var index in unicodeVowelSubset) {
    outputString += getUnicodeCharacter(unicodeVowelSubset[index]); //getUnicodeCharacter(codePt);
    outputString += stringToAppend;
  }
  output_text.innerHTML = outputString;
  output_text.value = outputString;

  updateHex(target, hex_target);
}

function convertLatinToUnicode(oldIn, newOut) {
  var input_text = document.getElementById(oldIn);
  var output_text = document.getElementById(newOut);
  var hex_output_id = "latin_hex";

    // Get flag indicating lower case conversion
    var convertToLower = document.getElementById("DoLower2").checked;
    var uText = latinToUnicode(input_text.value, convertToLower);
    output_text.innerHTML = uText;
    output_text.value = uText;

    updateHex(newOut, hex_output_id);
  }

// Fills the input with all the characters in the old Osage range.
function fillWithLatinOsage(target, hex_target, modifier) {
  var output_text = document.getElementById(target);
  var outputString = "";
  // Get mapping characters from the Latin map.
  var latin_keys = Object.keys(osage_latin_to_unicode_map);
  for (var index = 0; index < latin_keys.length; index ++) {
    var key = latin_keys[index];
    var uKey = key.toLowerCase();
    if (modifier != 'mono' || uKey == key) {
      outputString += key + ' ';
    }
  }
  output_text.innerHTML = outputString;
  output_text.value = outputString;
   updateHex(target, hex_target);
}

function fillWithLatinTests(target, hex_target, modifier) {
  var output_text = document.getElementById(target);
  var outputString = "HD hd HP H] HK UHU ";
  // Get mapping characters from the Latin map.
  output_text.innerHTML = outputString;
  output_text.value = outputString;
   updateHex(target, hex_target);
}

function fillWithLatinExtendedTests(target, hex_target, modifier) {
  var output_text = document.getElementById(target);
  var outputString = 
    "A a Ə ə E e I i O o U u\u000a" +
    "Ą ą Ə̨ ə Į į Ǫ ǫ\u000a" +
    "Aį aį Eį eį Oį oį Ai ai\u000a" +
    "Ā ā Ē ē Ī ī Ō ō Ū ū\u000a" +
    "\u0100\u0328 ą̄ Į̄ ī Ǭ ǭ\u000a" +
    "Á á É é Í í Ó ó Ú ú\u000a" +
    "    Ǫ́ ǫ́\u000a" +
    "Áį áį Éį éį Óį óį Ái ái\u000a" + 
    "                   \u000a" +
    "           ";
  output_text.innerHTML = outputString;
  output_text.value = outputString;
   updateHex(target, hex_target);
}

// Check text encoding.  If in Latin, return converted text in Unicode.
function convertLatinToOldOsage(oldIn, newOut) {
  var input_text = document.getElementById(oldIn);
  var output_text = document.getElementById(newOut);
  var hex_output_id = "old_hex";

    // Get flag indicating lower case conversion
    var convertToLower = document.getElementById("DoLower2").checked;
    var uText = latinToOldOsage(input_text.value, convertToLower);
    output_text.innerHTML = uText;
    output_text.value = uText;

    updateHex(newOut, hex_output_id);
  }

  // Check text encoding.
  function convertToUnicode(oldIn, newOut) {
    var input_text = document.getElementById(oldIn);
    var output_text = document.getElementById(newOut);
    var hex_output_id = "new_hex";

    // Call Unicode converter.
    // Get flags.
    var convertToLower = document.getElementById("DoLower").checked;
    var convertLatin = document.getElementById("convertLatin").checked;
    var clearOsageDot = document.getElementById("clearOsageDot").checked;
    var uText = oldOsageToUnicode(input_text.value,
      convertToLower, convertLatin, clearOsageDot);
    output_text.innerHTML = uText;
    output_text.value = uText;

    updateHex(newOut, hex_output_id);
  }

  // When an area is changed, set the hex characters, too.
  function updateHex(inArea, outArea) {
    var inText = document.getElementById(inArea).value;
    var hex_output = document.getElementById(outArea);
    var hexString = charsToHexString(inText);
    if (hex_output != null) {
      hex_output.value = hexString;
      hex_output.innerHTML = hexString;
    }
  }
  
  function onLayoutSelected(selector, controller, outputId) {
    var layoutCode = selector.value;
    controller.activateLayout(layoutCode);
    document.getElementById(outputId).focus();
    var vkbox = document.getElementById('kbd');

      if (layoutCode == "osa_traditional") {
        var field = document.getElementById("t1");
        field.style.fontFamily = "OldOsage";
        if (vkbox) {
          vkbox.style.fontFamily = "OldOsage";
        }
      }
      if (layoutCode == "osa") {
        var field = document.getElementById("t1");
        field.style.fontFamily = "Pawhuska";
        if (vkbox) {
          vkbox.style.fontFamily = "Pawhuska";
       }
      }
    }

  function toOsageFonts(area1, area2) {
    // Open a comparison window with the resulting text.
    var area1Elem = document.getElementById(area1);
    var text1 = area1Elem.value;

    text2 = "";
    if (area2 != "") {
      var area2Elem = document.getElementById(area2);
      var text2= area2Elem.value;
    }
    compareUrl = "/OsageFonts/?utext=" + text1 + "&osageText=" + text2;

    window.location=compareUrl;   
  }
