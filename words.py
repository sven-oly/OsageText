# -*- coding: utf-8 -*-
#!/usr/bin/env python

import json
import logging
import os
import urllib
import webapp2

from google.appengine.ext.webapp import template

# Show data from word list converted for human verification
class WordHandler(webapp2.RequestHandler):
    def get(self):
      fontList = []
      template_values = {'fontFamilies': fontList,
      }
      path = os.path.join(os.path.dirname(__file__), 'words.html')
      self.response.out.write(template.render(path, template_values))


# TODO: Get data and add next/previous
# Add approve
# Add controls for loading records
#     for saving new status
#     for getting records approved or not
#     for showing all records.

class GetDataHandler(webapp2.RequestHandler):
  def get(self):
    # Get info from client on which item.
    text = self.request.get("text", "")
    self.response.headers['Content-Type'] = 'application/json'   
    
    # TODO: fetch data
    # TODO: put data into return object  
    obj = { 
    }
    self.response.out.write(json.dumps(obj))