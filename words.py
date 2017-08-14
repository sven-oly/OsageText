# -*- coding: utf-8 -*-
#!/usr/bin/env python

import main
from userDB import getUserInfo

import csv
import json
import logging
import os
import StringIO

import urllib
import webapp2

from google.appengine.api import users

# Help from http://nealbuerger.com/2013/12/google-app-engine-import-csv-to-datastore/
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

from google.appengine.ext.webapp import template

# dbName will allow multiple sets of information to be stored and retrieved by that
# value. Added 14-Mar-2017

class OsagePhraseDB(db.Model):
  index = db.IntegerProperty()
  dbName = db.StringProperty(u'')
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)
  englishPhrase = db.StringProperty(multiline=True)
  osagePhraseLatin = db.StringProperty(u'')
  osagePhraseUnicode = db.StringProperty(u'')
  status = db.StringProperty('')
  comment = db.StringProperty('')
  reference = db.StringProperty('')  # Reference number or other identifier

  # Pointing to sound files by URL:
  soundFemaleLink = db.TextProperty('');
  soundMaleLink = db.TextProperty('');
  soundLinks = db.ListProperty(str, verbose_name='sound_files', default=[])


# The set of registered db names.
class OsageDbName(db.Model):
  dbName = db.StringProperty(u'')
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)
  default = db.StringProperty(u'')
  isTestDB = db.StringProperty('')


# Sound file info uploaded.
class UserSound(db.Model):
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)
  user = db.StringProperty('')
  blob_key = db.StringProperty('')


# Retrieves data at a given index and dbName via AJAX.
class GetWordsHandler(webapp2.RequestHandler):
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'

    print 'GetWordsHandler received.'
    self.response.out.write('GetWordsHandler received.\n')

  def get(self):
    user_info = getUserInfo(self.request.url)
    index = int(self.request.get('index', '1'))
    filterStatus = self.request.get('filterStatus', 'All')
    direction = int(self.request.get('direction', '0'))
    dbName = self.request.get('dbName', '')
    databases = self.request.GET.getall('databases')

    phraseKey = self.request.get('phraseKey', None)
    logging.info('phraseKey = %s' % phraseKey)
    if phraseKey:
      keyForPhrase = db.Key(encoded=phraseKey)
    else:
      keyForPhrase = None

    if keyForPhrase:
      # Get the pharse result from the key.
      result = db.get(keyForPhrase)
      logging.info('+++ Got object from key')
    else:
      #logging.info('GetWordsHandler databases = %s' % databases)
      #logging.info('GetWordsHandler index = %d, filterStatus=>%s<, direction = %d' %
      #   (index, filterStatus, direction))

      qdb = OsageDbName.all()
      dbNames = [p.dbName for p in qdb.run()]

      q = OsagePhraseDB.all()

      selectByDB = True
      #logging.info('GetWordsHandler DBNAME = %s' % dbName)
      if '*All*' in databases:
        logging.info('*All* in databases = %s' % databases)
        selectByDB = False

      if databases:
        q.filter('dbName IN', databases)
        # logging.info('GetWordsHandler FILTER by databases = %s' % databases)

      if filterStatus == 'All' or filterStatus == 'all':
        # Get the specified index, with no status filter.
        #logging.info('GetWordsHandler Going for index = %d' % index)
        q.filter("index =", index)
      else:
        # Set up to get next phrase with required status and index >= query index.
        #logging.info('FILTERING WITH status = %s, index >= %d' % (filterStatus, index))
        q.filter('status =', filterStatus)
        if selectByDB and databases:
          q.filter('dbName IN', databases)
          logging.info('GetWordsHandler FILTER WITH DATABASES: %s' % databases)
        if direction < 0:
          q.filter('index <=', index)
          q.order('-index')
        else:
          q.filter('index >=', index)
          q.order('index')

      result = q.get()  # Use get_multi for more than one?
      # END OF QUERY FOR RESULT.

    #logging.info('RESULT = %s' % (result))
    if result:
      index = result.index
      dbName = result.dbName
      oldtext = result.osagePhraseLatin
      utext = result.osagePhraseUnicode
      english = result.englishPhrase
      status = result.status
      comment = result.comment
      errorMsg = ''
      phraseKey = str(result.key())
    else:
      errorMsg = 'No phrase found'
      phraseKey = ''
      oldtext = utext = english = status = ''
      comment = ''

    # logging.info('PHRASE KEY = %s ' % phraseKey)
    logging.info('soundMaleLink: %s' % result.soundMaleLink)
    logging.info('soundFemaleLink: %s' % result.soundFemaleLink)

    obj = {
        'language': main.Language,
        'dbNames': dbNames,
        'index': index,
        'dbName': dbName,
        'phraseKey': phraseKey,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
        'status': status,
        'error': errorMsg,
        'comment': comment,
        'user_nickname': user_info[1],
        'user_logout': user_info[2],
        'user_login_url': user_info[3],
        'soundMaleLink': result.soundMaleLink,
        'soundFemaleLink': result.soundFemaleLink,
    }
    # logging.info('^^^^^^^ obj = %s' % obj)
    self.response.out.write(json.dumps(obj))

# Show data from word list converted for human verification
class WordHandler(webapp2.RequestHandler):
    def get(self):
      user_info = getUserInfo(self.request.url)
      fontList = []
      index = 1
      oldtext = self.request.get('oldtext', '')
      dbName = self.request.get('dbName', '')
      utext = self.request.get('utext', '')
      english = self.request.get('english', '')
      index = int(self.request.get('index', '1'))
      comment = self.request.get('comment', '')
      dbName = self.request.get('dbName', '')
      phraseKey = self.request.get('phraseKey', '')
      status = ''
      soundFemaleLink = ''
      soundMaleLink = ''

      q = OsagePhraseDB.all()
      currentEntries = 0
      for p in q.run():
        currentEntries += 1
      q.filter("index =", index)
      if dbName:
        logging.info("dbName filter by %s" % dbName)
        q.filter("dbName", dbName)
      result = q.get()

      dbq = OsageDbName.all()
      dbNameList = [p.dbName for p in dbq.run()]

      if result:
        oldtext = result.osagePhraseLatin
        dbName = result.dbName
        utext = result.osagePhraseUnicode
        english = result.englishPhrase
        status = result.status
        comment = result.comment
        soundFemaleLink = result.soundFemaleLink
        soundMaleLink = result.soundMaleLink
        logging.info('LINKS LINKS FFFF: %s' % soundFemaleLink)
        logging.info('LINKS LINKS MMMM: %s' % soundMaleLink)
        phraseKey = result.key()

      editOrAdmin = user_info[4]

      #logging.info('q = %s' % result)
      template_values = {
        'editOrAdmin': editOrAdmin,
        'language': main.Language,
        'index': index,
        'dbName': dbName,
        'phraseKey': phraseKey,
        'dbNames': dbNameList,
        'numEntries': currentEntries,
        'fontFamilies': fontList,
        'oldtext': oldtext,
        'utext': utext,
        'english': english,
        'comment': comment,
        'status': status,
        'fontFamilies': main.OsageFonts,
        'user_nickname': user_info[1],
        'user_logout': user_info[2],
        'user_login_url': user_info[3],
        'isAdmin': user_info[4],
        'soundFemaleLink': soundFemaleLink,
        'soundMaleLink': soundMaleLink,
        'showSounds': True,
      }
      # logging.info('WORDS = %s' % template_values)
      path = os.path.join(os.path.dirname(__file__), 'words.html')
      self.response.out.write(template.render(path, template_values))


# Show simple interface for CSV upload.
class SolicitUpload(webapp2.RequestHandler):
  def get(self):
    # upload_url = blobstore.create_upload_url('upload')
    upload_url = '/words/uploadCSV/'

    user_info = getUserInfo(self.request.url)

    #logging.info('$$$$$$$$$ upload_url %s' % upload_url)
    q = OsageDbName.all()
    dbNameList = [p.dbName for p in q.run()]
    logging.info('dbNameList = %s' % dbNameList)

    template_values = {
      'language': main.Language,
      'upload_url':upload_url,
      'dbNames': dbNameList,
    }
    path = os.path.join(os.path.dirname(__file__), 'wordsUpload.html')
    self.response.out.write(template.render(path, template_values))

# Add entries in the uploaded CSV to the data store.
# TODO: check for duplicates.
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
    #logging.info('### Starting at index %d' % numEntries)
    self.response.out.write('### Starting at index %d' % numEntries)
    startIndex = numEntries + 1
    currentIndex = startIndex
    stringReader = unicode_csv_reader(StringIO.StringIO(fileInfo))
    for row in stringReader:
      entry = processRow(currentIndex, row)
      currentIndex += 1
      numEntries += 1
      self.response.out.write(entry)

    #logging.info('### StartIndex = %d. %d new entries added' % (startIndex, numEntries - startIndex))
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
    user_info = getUserInfo(self.request.url)

    confirmClear = self.request.get('confirmClear', False)
    dbName = self.request.get('dbName', '')
    if not confirmClear:
      self.response.out.write('!!! Clearing DB %s not confirmed. No changes made.' %
        dbName)
      return

    logging.info('CLEAR DB %s' % dbName)

    q = OsagePhraseDB.all()
    numEntries = 0
    nullCount = 0
    numDeleted = 0
    # TODO: repeat until all are deleted.
    for p in q.run():
      numEntries += 1
      if not p.index:
        nullCount += 1
      if dbName == '*All*' or p.dbName == dbName:
        OsagePhraseDB.delete(p)
        numDeleted += 1

    self.response.out.write('!!! Delete %d null index entries.' % nullCount)
    self.response.out.write('!!! Deleted %d entries for DB %s total.' % (
      numDeleted, dbName))


# Rename all entries in a DB to a new DB
class RenameDB(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)

    confirmRename = self.request.get('confirmRename', False)
    oldDbName = self.request.get('oldDbName', '')
    newDbName = self.request.get('newDbName', '')
    if not confirmRename:
      self.response.out.write('!!! Renaming DB %s to %s not confirmed. No changes made.' %
                              (oldDbName, newDbName))
      return

    logging.info('RENAME DB %s to %s' % (oldDbName, newDbName))

    q = OsagePhraseDB.all()
    numEntries = 0
    nullCount = 0
    numRenamed = 0
    for p in q.run():
      numEntries += 1
      if p.dbName == oldDbName:
        p.dbName = newDbName
        p.put()
        numRenamed += 1

    self.response.out.write('!!! Renamed %d entries from %s to %s.' % (
      numRenamed, oldDbName, newDbName))


# Updates the status of an entry and sets the Unicode field.
class UpdateStatus(webapp2.RequestHandler):
  def get(self):
    index = int(self.request.get('index', '1'))
    dbName = self.request.get('dbName', '')
    newStatus = self.request.get('newStatus', 'Unknown')
    unicodePhrase = self.request.get('unicodePhrase', '')
    oldOsagePhrase = self.request.get('oldOsageData', '')
    comment = self.request.get('comment', '')
    dbName = self.request.get('dbName', '')
    phraseKey = self.request.get('phraseKey', '')

    logging.info("_+_+_+ Update phraseKey = %s" % phraseKey)
    # To get the database object more easily
    if phraseKey:
      keyForPhrase = db.Key(encoded=phraseKey)
    else:
      keyForPhrase = None

    logging.info('_+_+_+_+_+_+_+ Update index = %d, oldOsage = %s' % (index, oldOsagePhrase))

    if keyForPhrase:
      result = db.get(keyForPhrase)
      logging.info('+++ Got object from key')
    else:
      q = OsagePhraseDB.all()
      q.filter("index =", index)
      result = q.get()

    # TODO: Check for null result
    result.status = newStatus;
    result.comment = comment
    if dbName:
      result.dbName = dbName

    if oldOsagePhrase:
      result.osagePhraseLatin = oldOsagePhrase

    if unicodePhrase:
      result.osagePhraseUnicode = unicodePhrase
    result.put()

    # Send update back to client
    obj = {
      'language': main.Language,
      'index': index,
      'status' : result.status,
      'osagePhraseLatin' :  oldOsagePhrase,
    }
    self.response.out.write(json.dumps(obj))


class AddPhrase(webapp2.RequestHandler):
  def get(self):
    oldtext = self.request.get('oldtext', '')
    dbName = self.request.get('dbName', '')
    utext = self.request.get('utext', '')
    engtext = self.request.get('engtext', '')
    comment = self.request.get('comment', '')
    dbName = self.request.get('dbName', '')

    # Check if this already exists.
    q = OsagePhraseDB.all()
    q.filter('osagePhraseLatin =', oldtext)
    result = q.get()

    if result:
      # It's a duplicate. Return warning.
      message = 'This Osage message already exists at index %s' % result.index
    else:
      # It's not there so get new index and store.
      q = OsagePhraseDB.all()
      maxIndex = 0
      for p in q.run():
        if p.index > maxIndex:
          maxIndex = p.index
      entry = OsagePhraseDB(index=maxIndex + 1,
        dbName=dbName,
        englishPhrase=engtext,
        osagePhraseLatin=oldtext,
        osagePhraseUnicode=utext,
        comment=comment,
        soundFemaleLink='',
        soundMaleLink='',
        status='Unknown')
      entry.put()
      message = 'New Osage message added at index %s' % entry.index

    response = {
      'new_index': entry.index,
      'message': message,
    }
    self.response.out.write(json.dumps(response))


# Resets items from database.
class GetPhrases(webapp2.RequestHandler):
  def get(self):
    user_info = getUserInfo(self.request.url)

    filterStatus = self.request.get('filterStatus', '')
    dbName = self.request.get('dbName', '')
    databases = self.request.GET.getall('databases')
    if databases == '*All*' or '*All*' in databases:
      selectAllDB = True
      databases = []
    else:
      selectAllDB = False

    logging.info('  **** Databases = %s, selectAllDB = %s' % (databases, selectAllDB))

    q = OsagePhraseDB.all()
    if filterStatus:
      q.filter('status =', filterStatus)
    if not selectAllDB or databases:
      if type(databases) is not list:
        databases = [databases]
      q.filter('dbName IN', databases)
      logging.info('FILTER WITH DATABASES: %s' % databases)
    q.order('index')

    # All available databases.
    dbq = OsageDbName.all()
    dbNames = [p.dbName for p in dbq.run()]
    dbNameListChecked = []
    for db in dbNames:
      setcheck = db in databases
      dbNameListChecked.append({'dbName':db, 'checked':setcheck})
    # dbNameListChecked.append({'db':'All', 'checked':selectAllDB})

    logging.info('dbNames = %s' % dbNames)
    logging.info('dbNameListChecked = %s' % dbNameListChecked)
    logging.info('dbNameList = %s' % dbNames)

    # TODO: Make this user-specific.
    try:
      defaultDB = dbNames[0]
    except:
      defaultDB = None

    numEntries = 0
    entries = []
    nullIndexCount = 0
    for p in q.run():
      numEntries += 1

      if not p.index:
        nullIndexCount += 1
        entry = (p.index, p.englishPhrase, p.osagePhraseLatin, p.osagePhraseUnicode,
          p.status, p.dbName)
      entries.append(p)
    # TODO: get them, and sent to client
    template_values = {
      'language': main.Language,
      'entries': entries,
      'dbNames': dbNames,
      'dbNameListChecked': dbNameListChecked,
      'databases': databases,
      'dbName': defaultDB,
      'filter': filterStatus,
      'selectAllDB': selectAllDB,
      'user_nickname': user_info[1],
      'user_logout': user_info[2],
      'user_login_url': user_info[3],
      'isAdmin': user_info[4],
    }

    path = os.path.join(os.path.dirname(__file__), 'phrasesList.html')
    self.response.out.write(template.render(path, template_values))

# Uses blob. TODO: make this work.
class OldProcessUpload(webapp2.RequestHandler):
   def post(self):
     upload_files = self.get_uploads('file')
     #logging.info('$$$$$$$$$ upload_files %s' % upload_files[1])

     blob_info = upload_files[0]
     #logging.info('$$$$$$$$$ blob_info %s' % blob_info)

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
  #logging.info('!! index = %d     english= %s' % (index, english))
  # TODO: dbName
  entry = OsagePhraseDB(index=index,
    englishPhrase=english,
    osagePhraseLatin=osageLatin,
    osagePhraseUnicode='',
    status="Unknown",
    soundFemaleLink='',
    soundMaleLink='',
  )
  entry.put()
  return entry


class ProcessCSVUpload(webapp2.RequestHandler):
# http://stackoverflow.com/questions/2970599/upload-and-parse-csv-file-with-google-app-engine
  def post(self):

    #self.response.headers['Content-Type'] = 'text/plain'
    csv_file = self.request.POST.get('file')
    logging.info('ProcessCSVUpload csv_file = %s' % csv_file)
    dbName = self.request.POST.get('dbName', '')
    indexColumn = self.request.POST.get('indexColumn', '')
    osageColumn = self.request.POST.get('osageColumn', 'B')
    englishColumn = self.request.POST.get('englishColumn', 'D')
    commentColumn = self.request.POST.get('commentColumn', '')
    unicodeColumn = self.request.POST.get('unicodeColumn', '')
    referenceColumn = self.request.POST.get('referenceColumn', '')
    skipLines = int(self.request.POST.get('skipLines', '1'))
    skipEmptyLines = self.request.POST.get('skipEmptyLines', False)
    maxLines = int(self.request.POST.get('maxLines', -1))

    logging.info('unicodeColumn = %s' % unicodeColumn)

    logging.info('skip Empty Lines = %s' % skipEmptyLines)
    columns = [osageColumn, englishColumn, commentColumn, unicodeColumn]

    self.response.out.write('File %s to dbName: %s \n' % (csv_file, dbName))
    self.response.out.write('Columns: %s %s %s\n' % (osageColumn, englishColumn, commentColumn))
    self.response.out.write('Skip lines = %d\n' % skipLines)
    self.response.out.write('Skip empty lines = %s\n' % skipEmptyLines)
    self.response.out.write('maxLines = %s\n' % maxLines)

    fileReader = csv.reader(csv_file.file)
    lineNum = 0
    numProcessed = 0
    # Spreadsheet to index map. Update if more than 7 columns
    columnMap = {
      'A' : 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6,
      'a' : 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
    }

    # TODO: find maxIndex from existing entries in dbNam
    maxIndex = 0
    emptyLines = 0

    entries = []
    for row in fileReader:
      # row is now a list containing all the column data in that row
      if lineNum < skipLines:
        x = 1
        #self.response.out.write('Skipping line %d :  %s\n' % (lineNum, row))
      else:
        x = 0
        #self.response.out.write('%3d: %s \n' % (lineNum, row))

        try:
          indexValue = int(row[columnMap[indexColumn]])
        except:
          indexValue = maxIndex + 1
        try:
          englishPhrase = row[columnMap[englishColumn]].strip()
        except:
          englishPhrase = ''
        try:
          osagePhraseLatin = row[columnMap[osageColumn]].strip()
        except:
          osagePhraseLatin = ''
        try:
          comment = row[columnMap[commentColumn]].strip()
        except:
          comment = ''
        try:
          utext = row[columnMap[unicodeColumn]].strip()
        except:
          utext = ''
        try:
          reference = row[columnMap[referenceColumn]].strip()
        except:
          reference = ''

        #self.response.out.write('    E>%s<E \n' % (englishPhrase))
        #self.response.out.write('    O>%sO< \n' % (osagePhraseLatin))
        #self.response.out.write('    C>%s<C \n' % (comment))
        #self.response.out.write('    U>%s<Y\n' % (utext))

        if (skipEmptyLines and not englishPhrase and not osagePhraseLatin and
          not utext):
          emptyLines += 1
          #self.response.out.write('--- Skipping line %d: %s' % (lineNum, row))
          continue
        try:
          entry = OsagePhraseDB(
            index=indexValue,
            dbName=dbName,
            englishPhrase=englishPhrase.decode('utf-8'),
            osagePhraseLatin=osagePhraseLatin,
            osagePhraseUnicode=utext.decode('utf-8'),
            comment=comment,
            reference=reference,
            soundFemaleLink='',
            soundMaleLink='',
            status= 'Unknown')
          entry.put()
          entries.append(entry)
          numProcessed += 1
          maxIndex += 1
        except Exception as err:
          y = 1
          self.response.out.write('  Cannot set item %d: %s. Error=%s\n' % (lineNum, row, err))


        if maxLines > 0 and numProcessed > maxLines:
          self.response.out.write('\n Stopped after maximum %d processed' % (numProcessed))
          break

      lineNum += 1

    self.response.out.write('\n %d lines processed\n' % (numProcessed))

    template_values = {
      'language': main.Language,
      'dbname': dbName,
      'skipLines': skipLines,
      'columns': columns,
      'numberLoaded': numProcessed,
      'entries': entries,
      'emptyLines': emptyLines,
    }
    path = os.path.join(os.path.dirname(__file__), 'DBUploadResults.html')
    self.response.out.write(template.render(path, template_values))
