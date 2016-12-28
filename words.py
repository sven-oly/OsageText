# -*- coding: utf-8 -*-
#!/usr/bin/env python

import csv
import json
import logging
import os
import StringIO

import urllib
import webapp2

# Help from http://nealbuerger.com/2013/12/google-app-engine-import-csv-to-datastore/
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db


from google.appengine.ext.webapp import template

class OsagePhraseDB(db.Model):
    index = db.IntegerProperty()
    lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True,)
    englishPhrase = db.StringProperty(multiline=True)
    osagePhraseLatin = db.StringProperty(u'')
    osagePhraseUnicode = db.StringProperty(u'')
    status = db.StringProperty('')
  
class GetWordsHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'   

    print 'ConvertHandler get received.'
    self.response.out.write('ConvertHandler get received.\n')

  def get(self):
    index = int(self.request.get('index', '1'))
    q = OsagePhraseDB.all()
    q.filter("index =", index)
    result = q.get()
    if result:
      oldtext = result.osagePhraseLatin
      utext = result.osagePhraseUnicode
      english = result.englishPhrase
    else:
      oldtext = utext = english = ''
    obj = {
        'index': index,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
      }
    self.response.out.write(json.dumps(obj))

# Show data from word list converted for human verification
class WordHandler(webapp2.RequestHandler):
    def get(self):
      fontList = []
      index = 1
      oldtext = self.request.get('oldtext', '')
      utext = self.request.get('utext', '')
      english = self.request.get('english', '')
      index = int(self.request.get('index', '1'))
      q = OsagePhraseDB.all()
      q.filter("index =", index)
      result = q.get()
      if result:
        oldtext = result.osagePhraseLatin
        utext = result.osagePhraseUnicode
        english = result.englishPhrase
      logging.info('q = %s' % result)
      template_values = {
        'index': index,
        'fontFamilies': fontList,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
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

    self.response.headers['Content-Type'] = 'application/json'   
    
    # TODO: fetch data
    # TODO: put data into return object  
    obj = {

    }
    self.response.out.write(json.dumps(obj))


class SolicitUpload(webapp2.RequestHandler):
  def get(self):
    # upload_url = blobstore.create_upload_url('upload')
    upload_url = '/words/upload/'
    logging.info('$$$$$$$$$ upload_url %s' % upload_url)

    template_values = {'upload_url':upload_url}
    path = os.path.join(os.path.dirname(__file__), 'wordsUpload.html')
    self.response.out.write(template.render(path, template_values))


class ProcessUpload(webapp2.RequestHandler): 
  def post(self):
    fileInfo = self.request.get('file')
    self.response.out.write(fileInfo)

    logging.info('$$$$$$$$$ fileInfo = %s' % fileInfo)
    entries = process_csv(fileInfo)

    numEntries = 0
    stringReader = unicode_csv_reader(StringIO.StringIO(fileInfo))
    for row in stringReader:
      entry = processRow(numEntries, row)
      numEntries += 1
      #self.response.out.write(entry) 

    logging.info('### %d entries found', numEntries)
    self.response.out.write('\n\n### %d entries found' % numEntries) 


class OldProcessUpload(webapp2.RequestHandler): 
   def post(self):
     upload_files = self.get_uploads('file')
     logging.info('$$$$$$$$$ upload_files %s' % upload_files[1])

     blob_info = upload_files[0]
     logging.info('$$$$$$$$$ blob_info %s' % blob_info)
     
     entries = process_csv(blob_info)
     blobstore.delete(blob_info.key())  # optional: delete file after import
     
     self.response.headers['Content-Type'] = 'application/json'
     self.response.out.write(self.request.get('csv'))
     # filename = 'data/Approved_Words.Language.xlsx - Sheet1.csv'
     #file = open(os.path.join(os.path.dirname(__file__), filename)) 

     self.response.out.write(entries) 

# To handle UTF-8 input.
def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        
def processRow(index, row):
  english, osageLatin = row
  #logging.info('!!     english= %s' % english)
  entry = OsagePhraseDB(index=index,
    englishPhrase=english,
    osagePhraseLatin=osageLatin,
    osagePhraseUnicode='',
    status="unknown")
  entry.put()
  return entry


def process_csv(fileInfo):
  stringReader = unicode_csv_reader(StringIO.StringIO(fileInfo))
  entries = []
  for row in stringReader:
    english, osageLatin = row
    #logging.info('!!     english= %s' % english)
    entry = OsagePhraseDB(englishPhrase=english, osagePhraseLatin=osageLatin,
      osagePhraseUnicode='',
      status="unknown",
      lastUpdate=None)
    entry.put()
    entries.append(entry)
  return entries