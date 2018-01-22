# -*- coding: utf-8 -*-
#!/usr/bin/env python


# from docx import *

import csv
import json
import logging
import os
import StringIO

import webapp2

from google.appengine.ext.webapp import template


# Resets items from database.
class DocxTest(webapp2.RequestHandler):
  def get(self):
    #document = Document()

    #document.add_heading('Document Title', 0)

    template_values = {
    }

    path = os.path.join(os.path.dirname(__file__), 'docxText.html')
    self.response.out.write(template.render(path, template_values))

# Displatching for docx.
app = webapp2.WSGIApplication([
    ('/docx/test/', DocxTest),

], debug=True)