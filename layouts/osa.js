// Choctaw virtual keyboard.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// TODO: Complete this keyboard definition.

// Based on Osage tranditional keyboard
// Unicode output

var OSA_UNICODE_LAYOUT = {
  'id': 'osa',
  'title': 'Osage Unicode',
  'mappings': {
    '': {
      '': '{{\u0301}}1234567890-=' +
        '{{\ud801\udcd8\u0358}}{{\ud801\udcf7}}{{\ud801\udcdf}}{{\ud801\udcf2}}' +
	      '{{\ud801\udcf5}}{{\ud801\udcfb}}{{\ud801\udcf6}}{{\ud801\udce3}}' +
	      '{{\ud801\udcea}}{{\ud801\udcec}}[]\\' +
        '{{\ud801\udcd8}}{{\ud801\udcee}}{{\ud801\udcf0}}{{\u0358}}' +
	      '{{\ud801\udcf9}}{{\ud801\udce1}}{{\ud801\udcdb}}{{\ud801\udce4}}' +
	      '{{\ud801\udce7}}' + ';\'' +
        '{{\ud801\udcfa}}{{\ud801\udcf8}}{{\ud801\udcdd}}{{\ud801\udcef}}' +
	      '{{\ud801\udcdc}}{{\ud801\udce9}}{{\ud801\udce8}},./'
    },
    's': {
      '': '{{\u030b}}!@#$%^&*()_+' +
      '{{\ud801\udcb0\u0358}}{{\ud801\udccf}}{{\ud801\udcb7}}{{\ud801\udcca}}' +
	    '{{\ud801\udccd}}{{\ud801\udcd3}}{{\ud801\udcce}}{{\ud801\udcbb}}' +
	    '{{\ud801\udcc2}}{{\ud801\udcc4}}{}|' +
      '{{\ud801\udcb0}}{{\ud801\udcc6}}{{\ud801\udcc8}}{{\u0304}}' +
	    '{{\ud801\udcd1}}{{\ud801\udcb9}}{{\ud801\udcb3}}{{\ud801\udcbc}}' +
	    '{{\ud801\udcbf}}:"' +
      '{{\ud801\udcd2}}{{\ud801\udcd0}}{{\ud801\udcb5}}' +
	    '{{\ud801\udcc7}}{{\ud801\udcb4}}{{\ud801\udcc1}}{{\ud801\udcc0}}<>?'
    },
   'c': {  // alt-control
      '': '`{{¡}}™£¢\u221e§¶•{{\u25B8}}°–{{\u2260}}' +
        '{{\ud801\udcda}}{{\ud801\udceb}}{{\ud801\udce0}}{{\ud801\udcf3}}' +
          '{{\ud801\udcf4}}{{\u00a5}}' +
          '{{\u0328}}{{\ud801\udce3\u0358}}{{\ud801\udcea\u0358}}' +
          '{{\ud801\udced}}{{\u201C}}{{\u2018}}{{\u00ab}}' +
	  '{{\ud801\udcd9}}{{\ud801\udcef}}{{\ud801\udcf1}}{{}}' + 
	     '{{\u00a9}}{{\ud801\udce2}}{{\ud801\udcdb\u0358}}' +
	     '{{\ud801\udce5}}{{\ud801\udce6}}{{\u2026}}{{\u2039}}' +
	  '{{\ud801\udcfb}}{{\u2715}}{{\ud801\udcde}}{{\u2713}}' +
	     '{{}}{{}}{{}}{{\u2264}}{{\u2265}}{{\u00f7}}'
    },
   'sc': {  // shift-alt-control
      '': '~/€{{\u00be}}¼½†‡·„‚—±' +
        '{{\ud801\udcb2}}{{\ud801\udcc3}}{{\ud801\udcb8}}{{\ud801\udccb}}' +
          '{{\ud801\udccc}}{{}}{{}}{{\ud801\udcbb\u0358}}' +
          '{{\ud801\udcc2\u0358}}{{\ud801\udcc5}}{{\u201d}}{{\u2019}}{{\u00bb}}' +
        '{{\ud801\udcb1}}{{\ud801\udcc7}}{{\ud801\udcc9}}{{}}' + 
          '{{\u00ae}}{{\ud801\udcba}}{{\ud801\udcb3\u0358}}{{\ud801\udcbd}}' +
          '{{\ud801\udcbe}}:{{\u203a}}' +
	    '{{\ud801\udcd3}}{{\u2248}}{{\ud801\udcb6}}{{\u25c7}}' +
	      '{{}}{{\u03c0}}{{\u03bc}}{{}}' +
	      '{{}}{{\u00bf}}'
    },
    'l': {  // cap slock. qwerty
      '': '`1234567890-=' +
          'qwertyuiop[]\\' +
          'asdfghjkl;\'' +
          'zxcvbnm,./'
    },
    'sl': {  // shift-caps lock. QWERTY
      '': '~!@#$%^&*()_+' +
          'QWERTYUIOP{}|' +
          'ASDFGHJKL:"' +
          'ZXCVBNM<>?'
    }
  },
  'transform': {
    '"a' : '\u028a',
    '"A' : '\u01b1',
    '"e' : '\u028a\u0331',
    '"E' : '\u01b1\u0331',
    '"i' : '\u028a\u0301',
    '"I' : '\u01b1\u0301',
    '"E' : '\u01b1\u0301',
    '"o' : '\u028a\u0301\u0331',
    '"O' : '\u01b1\u0301\u0331',
    '"u' : 'Choctaw seal',
    '"y' : '\u00b7',
    '\'a': 'a\u0331',
    '\'e': 'e\u0331',
    '\'i': 'i\u0331',
    '\'o': 'o\u0331',
    '\'u': 'u\u0331',
    '`a': 'a\u0301',
    '`e': 'e\u0301',
    '`i': 'i\u0301',
    '`o': 'o\u0301',
    '`u': 'u\u0301',
    '^a': 'a\u0301\u0330',
    '^e': 'e\u0301\u0330',
    '^i': 'i\u0301\u0330',
    '^o': 'o\u0301\u0330',
    '^u': 'u\u0301\u0330',
    '\ud801\udce1\ud801\udcec': '\ud801\udced',  // h-pa
    '\ud801\udce1\ud801\udcc4': '\ud801\udcc5',  // H-PA
    '\ud801\udcb9\ud801\udcec': '\ud801\udced',  // H-pa
    '\ud801\udcb9\ud801\udcc4': '\ud801\udcc5',  // H-PA

    '\ud801\udce1\ud801\udce4': '\ud801\udce5',  // h-ka
    '\ud801\udce1\ud801\udcbc': '\ud801\udcbd',  // h-KA
    '\ud801\udcb9\ud801\udce4': '\ud801\udce5',  // H-ka
    '\ud801\udcb9\ud801\udcbc': '\ud801\udcbd',  // H-KA
    
    '\ud801\udce1\ud801\udcf0': '\ud801\udcf1',  // h-ta
    '\ud801\udce1\ud801\udcc8': '\ud801\udcc9',  // h-ta
    '\ud801\udcb9\ud801\udcf0': '\ud801\udcf1',  // H-ta
    '\ud801\udcb9\ud801\udcc8': '\ud801\udcc9',  // H-TA

    '\ud801\udce1\ud801\udcdd': '\ud801\udcde',  // h-cha 
    '\ud801\udce1\ud801\udcb5': '\ud801\udcb6',  // h-CHA 
    '\ud801\udcb9\ud801\udcdd': '\ud801\udcde',  // H-cha
    '\ud801\udcb9\ud801\udcb5': '\ud801\udcb6',  // H-CHA
    
    '\ud801\udce1\ud801\udcf2': '\ud801\udcf3',  // h-sha 
    '\ud801\udce1\ud801\udcca': '\ud801\udccb',  // h-SHA 
    '\ud801\udcb9\ud801\udcf2': '\ud801\udcf3',  // H-sha 
    '\ud801\udcb9\ud801\udcca': '\ud801\udccb',  // H-SHA    

    '\ud801\udcb0\ud801\udcb0': '\ud801\udcb0\u0304',  // AA    
    '\ud801\udcd8\ud801\udcd8': '\ud801\udcd8\u0304',  // aa    
    '\ud801\udcb7\ud801\udcb7': '\ud801\udcb7\u0304',  // EE
    '\ud801\udcdf\ud801\udcdf': '\ud801\udcdf\u0304',  // AA    
    '\ud801\udcc2\ud801\udcc2': '\ud801\udcc2\u0304',  // OO
    '\ud801\udcea\ud801\udcea': '\ud801\udcea\u0304',  // oo
    '\ud801\udcbb\ud801\udcbb': '\ud801\udcbb\u0304',  // II
    '\ud801\udce3\ud801\udce3': '\ud801\udce3\u0304',  // ii
    '\ud801\udcce\ud801\udcce': '\ud801\udcce\u0304',  // II
    '\ud801\udcf6\ud801\udcf6': '\ud801\udcf6\u0304',  // ii
    }
};

// Load the layout and inform the keyboard to switch layout if necessary.
google.elements.keyboard.loadme(OSA_UNICODE_LAYOUT);
