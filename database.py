# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Functions that handle database management

import main
import words
from userDB import getUserInfo


import logging
import os

import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

# Help from http://nealbuerger.com/2013/12/google-app-engine-import-csv-to-datastore/

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

# Clear out the entire phrase data store, or part of it (eventually)
class ResetDBEntries(webapp2.RequestHandler): 
  def get(self):
    user_info = getUserInfo(self.request.url)

    # TODO: Get from request
    oldDbName = ''
    newDbName = 'Approved Words'   
    q = words.OsagePhraseDB.all()
    numEntries = 0
    numReset = 0
    # TODO: repeat until all are reset.
    for p in q.run():
      numEntries += 1
      if p.dbName is None or p.dbName == oldDbName:
        p.dbName = newDbName
        p.put()
        numReset += 1
    # TODO: delete them, with message.
    self.response.out.write('!!! Total DB entries = %d.' % numEntries)
    self.response.out.write('!!! Reset dbname from >%s< to >%s< for %d entries total.' % (
        oldDbName, newDbName, numReset))
        

class ManageDbName(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)

    submitType =  self.request.get('deleteDB', '')
    dbName = self.request.get('dbName', '')
    clear = self.request.get('clear', '')
    confirmDelete = self.request.get('confirmDelete', None)
    confirmAdd = self.request.get('confirmAdd', None)
    
    q = words.OsageDbName.all()
    if submitType == "deleteDB" and dbName:
      if not confirmDelete:
        self.response.out.write('Deleting db Name = %s is not confirmed.\n' % dbName)
        return
      # Wipe out DB
      for p in q.run():
        pName = p.dbName
        if dbName == "*ALL*" or dbName == pName:
          words.OsageDbName.delete(p)
          self.response.out.write('Deleted db Name = %s.\n' % dbName)
      return
      
    # No name -> return list of all.
    if not dbName:
      nameList = []
      for p in q.run():
        nameList.append(p.dbName)
      self.response.out.write('db Names = %s.\n' % nameList)
      return

    q.filter("dbName =", dbName)
    result = q.get()
    
    if not confirmAdd:
      self.response.out.write('Adding db Name = %s is not confirmed.\n' % dbName)
      return

    if result:
      self.response.out.write('db Name = %s is already defined.\n' % dbName)
    else:
      entry = words.OsageDbName(dbName=dbName);
      entry.put()
      self.response.out.write('db Name = %s has been added.\n' % dbName)


# Show simple interface for CSV upload.
class SolicitUpload(webapp2.RequestHandler):
  def get(self):
    # upload_url = blobstore.create_upload_url('upload')
    upload_url = '/words/uploadCSV/'

    user_info = getUserInfo(self.request.url)

    #logging.info('$$$$$$$$$ upload_url %s' % upload_url)
    q = words.OsageDbName.all()
    dbNameList = [p.dbName for p in q.run()]
    logging.info('dbNameList = %s' % dbNameList)

    template_values = {
      'language': main.Language,
      'upload_url':upload_url,
      'dbNames': dbNameList,
    }
    path = os.path.join(os.path.dirname(__file__), 'wordsUpload.html')
    self.response.out.write(template.render(path, template_values))


# Dispatch requests.
app = webapp2.WSGIApplication([

    ('/db/manageDB/', SolicitUpload),
    ('/db/handleDB/', ManageDbName),
    ('/db/resetDbEntries/', ResetDBEntries),

], debug=True)
