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

// TODO: Complete the Unicode mapping.

var OSA_TRADITIONAL_LAYOUT = {
  'id': 'osa_traditional',
  'title': 'Osage Traditional',
  'mappings': {
    '': {
      '': '`12345{{\uf05e}}7890-=' +
          '{{}}{{\uf057}}{{\uf045}}{{}}{{\uf054}}{{\uf059}}{{\uf055}}' +
	  '\uf049\uf04f\uf050\uf05b\uf05d\uf05c' +
          '{{\uf041}}{{\uf053}}{{\uf044}}{{}}{{}}\uf048\uf04a\uf04b\uf04c\uf03b\uf060' +
          '{{\uf05a}}{{\uf058}}{{\uf043}}{{\uf056}}{{\uf042}}{{\uf04e}}' +
	  '{{\uf04d}}{{\uf03f}}.{{\uf02f}}'
    },
    's': {
      '': '~!@#$%^&*()_+' +
          '{{}}{{}}{{\uf065}}{{}}{{}}{{}}{{}}{{}}{{\uf06f}}{{}}{}|' +
          '{{\uf061}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}{{}}:"' +
          '{{}}{{}}{{}}{{}}{{}}{{}}{{}}<>?'
    },
    'l': {
      '': '`1234567890-=' +
          'qwertyuiop[]\\' +
          'asdfghjkl;\'' +
          'zxcvbnm,./'
    },
    'sl': {
      '': '~!@#$%^&*()_+' +
          'QWERTYUIOP{}|' +
          'ASDFGHJKL:"' +
          'ZXCVBNM<>?'
    }
  }
};

// Load the layout and inform the keyboard to switch layout if necessary.
google.elements.keyboard.loadme(OSA_TRADITIONAL_LAYOUT);
