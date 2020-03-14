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

// For typing dictionary entries in Osage Latin orthography
var OSA_DICTIONARY = {
  'id': 'osa_dict',
  'title': 'Osage Dictionary',
  'mappings': {
    ',c': {
      '': '`1234567890-=' +
          'qwe{{\u030c}}t{{\u1d95}}uiop[]\\' +
          'as{{\u00f0}}{{\u02c0}}{{\u0263}}hjkl;{{\u0301}}' +
          'zxc{{\u0328}}bnm,./'
    },
    's,sc': {
      '': '~!@#$%^&*()_+' +
          'QWERTYUIOP{}|' +
          'AS{{\u00d0}}F{{\u0194}}HJKL:"' +
          'ZXCVBNM<>?'
    },
    'l,cl': {
      '': '`1234567890-=' +
          'qwertyuiop[]\\' +
          'asdfghjkl;\'' +
          'zxcvbnm,./'
    },
    'sl,scl': {
      '': '~!@#$%^&*()_+' +
          'QWERTYUIOP{}|' +
          'ASDFGHJKL:"' +
          'ZXCVBNM<>?'
    }
  },
  'transform': {
    'a\u0328': '\u0105',
    'A\u0328': '\u0104',
    'e\u0328': '\u0119',
    'E\u0328': '\u0118',
    'i\u0328': '\u012f',
    'I\u0328': '\u012e',
    'o\u0328': '\u01eb',
    'O\u0328': '\u01ea',
    'u\u0328': '\u0173',
    'U\u0328': '\u0172',
    'a\u0301': '\u00e1',
    'A\u0301': '\u00c1',
    'e\u0301': '\u00e9',
    'E\u0301': '\u00c9',
    'i\u0301': '\u00ed',
    'I\u0301': '\u00cd',
    'o\u0301': '\u00f3',
    'O\u0301': '\u00d3',
    'u\u0301': '\u00fa',
    'U\u0301': '\u00da',
  }
};

// Load the layout and inform the keyboard to switch layout if necessary.
google.elements.keyboard.loadme(OSA_DICTIONARY);
