# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import re
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
    logging.info('games WordSearchHandler')

    user_info = getUserInfo(self.request.url)
    user = users.get_current_user()
    rawWordList = self.request.get('words', '')

    #wordList = re.findall(r"[\w']+", rawWordList)
    #logging.info('games WordSearchHandler wordList = %s' % wordList)
    #grid, answers, words = wordsearch.generateWordsGrid(wordList)

    #logging.info('games WordSearchHandler grid = %s' % grid)
    #logging.info('games WordSearchHandler answers = %s' % answers)
    #logging.info('games WordSearchHandler words = %s' % words)

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
    logging.info('games GenerateWordSearchHandler')
    user_info = getUserInfo(self.request.url)
    user = users.get_current_user()

    rawWordList = self.request.get('words', '')

    wordList = re.findall(r"[\w']+", rawWordList)
    #logging.info('games WordSearchHandler wordList = %s' % wordList)

    grid, answers, words, grid_width = wordsearch.testGrid()

    #logging.info('games WordSearchHandler grid = %s' % grid)
    #logging.info('games WordSearchHandler answers = %s' % answers)
    #logging.info('games WordSearchHandler words = %s' % words)

    template_values = {
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
      'language': main.Language,
      'grid': grid,
      'answers': answers,
      'words': words,
      'grid_width': grid_width,
    }
    self.response.out.write(json.dumps(template_values))


class TestHandler(webapp2.RequestHandler):
  def get(self):
    logging.info('games TestHandler')

app = webapp2.WSGIApplication([
    ('/games/wordsearch/', WordSearchHandler),
    ('/games/generatewordsearch/', GenerateWordSearchHandler),
    ('/games/test/', TestHandler),
], debug=True)