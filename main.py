# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

from userDB import getUserInfo

import blobstorage
import database
import userDB
import words

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

# The Unicode fonts from Osage Nation.
OsageFonts = ['Pawhuska', 'Wynona', 'Avant', 'Barnsdall', 'Nelagoney',
              'Prue', 'Wazhezhe', 'GadugiBeta2', 'GadugiBoldBeta2',
              'NotoSansOsage_alpha', 'NotoSansOsage']

Language = 'Osage'

class MainHandler(webapp2.RequestHandler):
    def get(self):
      user_info = getUserInfo(self.request.url)

      oldOsageInput = self.request.get("text", "")
      unicodeInput = self.request.get("utext", "")
      latinInput = self.request.get("latintext", "")

      template_values = {
        'osageInput': oldOsageInput,
        'unicodeInput': unicodeInput,
        'latinInput': latinInput,
        'fontFamilies': OsageFonts,
        'user_nickname': user_info[1],
        'user_logout': user_info[2],
        'user_login_url': user_info[3],
        'isAdmin': user_info[4],
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
    user_info = getUserInfo(self.request.url)
    utext = self.request.get("utext", "")
    osageText = self.request.get("osageText", "")
    template_values = {
      'scriptName': 'Osage',
      'fontFamilies': OsageFonts,
      'osageText': osageText,
      'utext': utext,
      'language': Language,
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
    }

    path = os.path.join(os.path.dirname(__file__), 'osageFonts.html')
    self.response.out.write(template.render(path, template_values))

class OsageKeyboard(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url, self.request.url)
    template_values = {
      'fontFamilies': OsageFonts,
      'language': Language,
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
    }

    path = os.path.join(os.path.dirname(__file__), 'keyboard_osa.html')
    self.response.out.write(template.render(path, template_values))

class OsageUload(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)
    infile = self.request.get("infile", "")
    outfile = self.request.get("outfile", "")
    template_values = {
      'infile': infile,
      'outfile': outfile,
      'language': Language,
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
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


class LoginPageHandler(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)
    user = users.get_current_user()
    #logging.info(' ***** AUTH_DOMAIN = %s' %os.environ.get('AUTH_DOMAIN'))
    logging.info('UUUUU = %s', user)
    if user:
      nickname = user.nickname()
      logout_url = users.create_logout_url('/')
      greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
        nickname, logout_url)
      login_url = None
    else:
      nickname = None
      logout_url = None
      login_url = users.create_login_url('/')
      greeting = '<a href="{}">Sign in</a>'.format(login_url)

    logging.info('UUUUU greeting = %s', greeting)

    #self.response.write(
    #  '<html><body>{}</body></html>'.format(greeting))

    template_values = {
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
      'language': Language,
    }
    path = os.path.join(os.path.dirname(__file__), 'login.html')
    self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/OsageConverter/', MainHandler),
    ('/OsageConverter/test/', ConverterTestHandler),
    ('/OsageFonts/', OsageFontTest),
    ('/keyboard/', OsageKeyboard),
    ('/downloads/', OsageDownload),
    ('/upload/', OsageUload),

    ('/login/', LoginPageHandler),

    ('/words/', words.WordHandler),
    ('/words/addPhrase/', words.AddPhrase),
    ('/words/clear/', words.ClearWords),
    ('/words/renameDB/', words.RenameDB),
    ('/words/getWords/', words.GetWordsHandler),
    ('/words/getPhrases/', words.GetPhrases),
    ('/words/startUpload/', words.SolicitUpload),
    ('/words/updateStatus/', words.UpdateStatus),
    ('/words/upload/', words.ProcessUpload),
    ('/words/uploadCSV/', words.ProcessCSVUpload),
    ('/db/manageDB/', words.SolicitUpload),
    ('/db/handleDB/', database.ManageDbName),
    ('/db/resetDbEntries/', database.ResetDBEntries),
    ('/slides/', ProcessSlides),

    ('/users/', userDB.showUsers),
    ('/users/manage/', userDB.manageUsers),
    ('/users/add/', userDB.addUser),
    ('/users/clear/', userDB.clearUsers),

    ('/sound/showupload/', blobstorage.SoundUploadFormHandler),
    ('/sound/view/', blobstorage.ViewSoundHandler),
    ('/sound/listall/', blobstorage.SoundListHandler),
    ('/sound/viewall/', blobstorage.SoundDataViewerHandler),
    ('/sound/uploadtodbitem/', blobstorage.SoundUploadUI),
    ('/sound/uploadSoundForPhrase/', blobstorage.SoundFileUploadHandler),

    ('/sound/start/', blobstorage.CreateAndReadFileHandler),
    ('/sound/upload/', blobstorage.SoundUploadHandler),

], debug=True)
