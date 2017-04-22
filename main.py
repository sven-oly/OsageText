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

import words

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

# The Unicode fonts from Osage Nation.
OsageFonts = ['Gadugi', 'NotoSansOsage', 'Pawhuska', 'Wynona', 'Avant', 'Barnsdall', 'Nelagoney', 
  'Prue', 'Wazhezhe']

Language = 'Osage'

class MainHandler(webapp2.RequestHandler):
    def get(self):
      oldOsageInput = self.request.get("text", "")
      unicodeInput = self.request.get("utext", "")
      latinInput = self.request.get("latintext", "")

      template_values = {
        'osageInput': oldOsageInput,
        'unicodeInput': unicodeInput,
        'latinInput': latinInput,
        'fontFamilies': OsageFonts,
      }
      path = os.path.join(os.path.dirname(__file__), 'osage.html')
      self.response.out.write(template.render(path, template_values))     

class ConverterTestHandler(webapp2.RequestHandler):
  def get(self):
    utext = self.request.get("utext", "")
    osageText = self.request.get("osageText", "")
    template_values = {
      'fontFamilies': OsageFonts,
      'osageText': osageText,
      'utext': utext,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'testConvert.html')
    self.response.out.write(template.render(path, template_values))

class OsageFontTest(webapp2.RequestHandler):
  def get(self):
    utext = self.request.get("utext", "")
    osageText = self.request.get("osageText", "")
    template_values = {
      'scriptName': 'Osage',
      'fontFamilies': OsageFonts,
      'osageText': osageText,
      'utext': utext,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'osageFonts.html')
    self.response.out.write(template.render(path, template_values))

class OsageKeyboard(webapp2.RequestHandler):
  def get(self):
    template_values = {
      'fontFamilies': OsageFonts,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'keyboard_osa.html')
    self.response.out.write(template.render(path, template_values))
        
class OsageUload(webapp2.RequestHandler):
  def get(self):
    infile = self.request.get("infile", "")
    outfile = self.request.get("outfile", "")
    template_values = {
      'infile': infile,
      'outfile': outfile,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'osageUpload.html')
    self.response.out.write(template.render(path, template_values))

class OsageDownload(webapp2.RequestHandler):
  def get(self):
    infile = self.request.get("infile", "")
    outfile = self.request.get("outfile", "")
    template_values = {
      'infile': infile,
      'outfile': outfile,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'osageDownloads.html')
    self.response.out.write(template.render(path, template_values))


## TODO: Finish this.
class ProcessSlides(webapp2.RequestHandler):

  def get(self):
    # Default for testing.
    slideID = self.request.get("slideID", "1ENL72hoOv5dn_YTaT3dSDYH1818uHKndqQaqZa4sThI")
    outfile = self.request.get("outfile", "")
    template_values = {
      'slideID': slideID,
      'outfile': outfile,
      'language': Language,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'slideConvert.html')
    self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OsageConverter/', MainHandler),
    ('/OsageConverter/test/', ConverterTestHandler),
    ('/OsageFonts/', OsageFontTest),
    ('/keyboard/', OsageKeyboard), 
    ('/downloads/', OsageDownload), 
    ('/upload/', OsageUload), 

    ('/words/', words.WordHandler),
    ('/words/addPhrase/', words.AddPhrase),
    ('/words/clear/', words.ClearWords),
    ('/words/getWords/', words.GetWordsHandler),
    ('/words/getPhrases/', words.GetPhrases),
    ('/words/startUpload/', words.SolicitUpload),
    ('/words/updateStatus/', words.UpdateStatus),
    ('/words/upload/', words.ProcessUpload),
    ('/words/uploadCSV/', words.ProcessCSVUpload),
    ('/words/dbName/', words.AddDbName),
    ('/slides/', ProcessSlides),   
 
  ], debug=True)
    