# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import main

import wordsearch

from userDB import getUserInfo

import blobstorage
import userDB

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template


class WordSearchHandler(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)
    user = users.get_current_user()

    template_values = {
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
      'language': main.Language,
    }
    path = os.path.join(os.path.dirname(__file__), 'wordsearch.html')
    self.response.out.write(template.render(path, template_values))


class GenerateWordSearchHandler(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)
    user = users.get_current_user()

    template_values = {
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
      'language': main.Language,
    }
    path = os.path.join(os.path.dirname(__file__), 'wordsearch.html')
    self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/games/wordsearch/', WordSearchHandler),
    ('/games/generatewordsearch/', GenerateWordSearchHandler),
], debug=True)
