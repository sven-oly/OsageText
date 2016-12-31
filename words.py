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


# Retrieves data at a given index via AJAX. 
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
      status = result.status
    else:
      oldtext = utext = english = status = ''
    obj = {
        'index': index,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
        'status': status,
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
      status = ''

      q = OsagePhraseDB.all()
      currentEntries = 0
      for p in q.run():
        currentEntries += 1
      q.filter("index =", index)
      result = q.get()

      if result:
        oldtext = result.osagePhraseLatin
        utext = result.osagePhraseUnicode
        english = result.englishPhrase
        status = result.status
      logging.info('q = %s' % result)
      template_values = {
        'index': index,
        'numEntries': currentEntries,
        'fontFamilies': fontList,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
        'status': status
      }
      path = os.path.join(os.path.dirname(__file__), 'words.html')
      self.response.out.write(template.render(path, template_values))


# TODO: Add approve
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

    # Update with new data.
    # TODO: check for duplicates
    q = OsagePhraseDB.all()
    numEntries = 0
    for p in q.run():
      numEntries += 1
    logging.info('### Starting at index %d' % numEntries)
    self.response.out.write('### Starting at index %d' % numEntries) 
    startIndex = numEntries + 1
    currentIndex = startIndex
    stringReader = unicode_csv_reader(StringIO.StringIO(fileInfo))
    for row in stringReader:
      entry = processRow(currentIndex, row)
      currentIndex += 1
      numEntries += 1
      self.response.out.write(entry) 

    logging.info('### StartIndex = %d. %d new entries added' % (startIndex, numEntries - startIndex))
    self.response.out.write('### StartIndex = %d. %d new entries added' % (startIndex, numEntries - startIndex)) 
    q = OsagePhraseDB.all()
    currentEntries = 0
    for p in q.run():
      currentEntries += 1
    self.response.out.write('!!! Current entries now = %d.' %
      (currentEntries)) 


# Clear out the entire phrase data store, or part of it (eventually)
class ClearWords(webapp2.RequestHandler): 
  def get(self):
    q = OsagePhraseDB.all()
    numEntries = 0
    nullCount = 0
    for p in q.run():
      numEntries += 1
      if not p.index:
        nullCount += 1
      OsagePhraseDB.delete(p)
    # TODO: delete them, with message.
    self.response.out.write('!!! Will delete %d null index entries.' % nullCount)
    self.response.out.write('!!! Will delete all of the %d entries.' % numEntries)


# Gets all the phrase data store, or part of it (eventually)
class UpdateStatus(webapp2.RequestHandler): 
  def get(self):
    index = int(self.request.get('index', '1'))
    newStatus = self.request.get('newStatus', 'Unknown')

    logging.info('UpdateStatus: index = %d, newStatus = %s' % (index, newStatus))

    q = OsagePhraseDB.all()
    q.filter("index =", index)
    result = q.get()

    result.status = newStatus;
    result.put()
    
    # Send update back to client
    obj = {
      'index': index,
      'status' : result.status,   
    }
    self.response.out.write(json.dumps(obj))

  
 # Resets status for given item.
class GetPhrases(webapp2.RequestHandler): 
  def get(self):
    q = OsagePhraseDB.all()
    numEntries = 0
    entries = []
    nullIndexCount = 0
    for p in q.run():
      numEntries += 1
      if not p.index:
        nullIndexCount += 1
      entry = (p.index, p.englishPhrase, p.osagePhraseLatin, p.osagePhraseUnicode,
        p.status)
      entries.append(entry)
    # TODO: get them, and sent to client
    obj = {
      'entries': entries   
    }
    self.response.out.write('!!! %d entries. %d with null index' % (numEntries, nullIndexCount))
    self.response.out.write(json.dumps(obj))
  
# Uses blob. TODO: make this work.
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
  logging.info('!! index = %d     english= %s' % (index, english))
  entry = OsagePhraseDB(index=index,
    englishPhrase=english,
    osagePhraseLatin=osageLatin,
    osagePhraseUnicode='',
    status="Unknown")
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
      status="Unknown",
      lastUpdate=None)
    entry.put()
    entries.append(entry)
  return entries