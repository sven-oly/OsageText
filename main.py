# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

# The Unicode fonts from Osage Nation.
OsageFonts = ['Pawhuska', 'Wynona', 'Avant', 'Barnsdall', 'Nelagoney', 
  'Prue', 'Wazhezhe']

class MainHandler(webapp2.RequestHandler):
    def get(self):
      cwd = os.getcwd()

      template_values = {'fontFamilies': OsageFonts,
        'cwd': cwd,
      }
      path = os.path.join(os.path.dirname(__file__), 'osage.html')
      self.response.out.write(template.render(path, template_values))
      

class OsageFontTest(webapp2.RequestHandler):
  def get(self):
    template_values = {'fontFamilies': OsageFonts,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'osageFonts.html')
    self.response.out.write(template.render(path, template_values))

class OsageKeyboard(webapp2.RequestHandler):
  def get(self):
    template_values = {'fontFamilies': OsageFonts,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'keyboard_osa.html')
    self.response.out.write(template.render(path, template_values))
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OsageFonts/', OsageFontTest),
    ('/keyboard/', OsageKeyboard), 

	], debug=True)
    