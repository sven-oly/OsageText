# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

# Testing blobstorage upload for sound files, data, etc.
# Started 7-June-2017

# Based on https://cloud.google.com/appengine/docs/standard/python/blobstore/


from userDB import getUserInfo

import database
import main
import userDB
import words

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

import cloudstorage as gcs

from google.appengine.api import app_identity
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop


# Reference: https://cloud.google.com/appengine/docs/standard/python/blobstore/#Python_Uploading_a_blob
class CreateAndReadFileHandler(webapp2.RequestHandler):
    def get(self):
        user_info = getUserInfo(self.request.url)

        bucket_name = app_identity.get_default_gcs_bucket_name()

        param = 'general_parameter_1234'
        upload_url = '/sound/upload/'  # ?parameter=%s' % param
        upload_url = blobstore.create_upload_url(upload_url,
                                                 gs_bucket_name=bucket_name)
        logging.info('CreateAndReadFileHandler bucket_name: %s' % bucket_name)
        logging.info('CreateAndReadFileHandler upload_url: %s' % upload_url)

        self.response.out.write("""
       <html><body>
       <form action="{0}" method="POST" enctype="multipart/form-data">
         Upload File: <input type="file" name="file"><br>
         <input type="input" value="test what's passed to blob upload">
         <input type="submit" name="submit" value="Submit">
       </form>
       <p>Debug: upload_url = {0}
       </body></html>""".format(upload_url, upload_url))

        # [START SoundUploadHandler]

class SoundUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
          try:
            logging.info('SOUND UPLOAD handler!')
            upload_list = self.get_uploads()
            logging.info(' get_uploads = (%d) %s' % (len(upload_list), upload_list))
            # Other parameters?
            try:
              other = self.post('parameter', 'NONE FOUND')
              logging.info('@#@#@# parameter = %s' % other)
            except:
              other = 'NONE'
              logging.info('@#@#@# Cannot get parameter from self.')

            upload = upload_list[0]
            logging.info(' upload =  %s' % (upload))
            logging.info(' ####### upload key =  %s' % (upload.key()))
            logging.info(' ####### upload content type =  %s' % (upload.content_type))
            logging.info(' upload type =  %s' % (type(upload)))
            logging.info(' upload gs_object_name =  %s' % (upload.gs_object_name))

            try:
              filename = upload.filename
              logging.info(' upload filename =  %s' % (filename))
            except:
              logging.info(' Cannot get filename from upload.')

            #try:
            #  logging.info(' FFFFFFFFF upload fields =  %s' % (
            #      upload.__dict__()))
            #except:
            #  logging.info('  CANNOT get upload fields %s' % upload);

            logging.info('ABOUT TO DO PUBLIC URL')
            try:
              public_url = upload.gs_object_name
              logging.info('%%% public_url = %s!' % public_url)
            except:
              logging.info('SOUND UPLOAD handler. Cannot get public_url!')

            try:
              my_url = "https://osagelanguagetools.appspot.com.storage.googleapis.com/%s" % filename
              logging.info(' PUBLIC URL% %s' % my_url)
            except:
              logging.info(' Cannot make my url')

            try:
              user = users.get_current_user().user_id(),
              logging.info('SOUND UPLOAD: upload = %s, user = %s, key=%s' %
                           (upload, user, upload.key()))
            except:
              logging.info('SOUND UPLOAD handler. Cannot get user!')

            try:
              logging.info('Trying redirect!')
              redirect_target = '/sound/uploadresults/%s?%s' % (
                  upload.key(), 'parameter=%s' % other)
              logging.info('Target = %s' % redirect_target)
              self.redirect(redirect_target)
            except:
              logging.info('SOUND UPLOAD handler. Cannot create UserSound!')

            self.redirect('/sound/uploadresults/' % upload.key())

          except:
            self.error(500)
            # [END SoundUploadHandler]


class SoundUploadResults(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, sound_key):
      logging.info('@@@@@@@ SoundUploadResults: %s' % sound_key)
      try:
        parameter = self.get('parameter', 'NO PARAMETER')
        logging.info('PARAMETER = %s' % parameter)
      except:
        logging.info('NO PARAMETER')

      # TODO:(ccornelius) can anything else be done with this?
      if not blobstore.get(sound_key):
        logging.info('ERROR!!!')
        self.error(404)
      else:
        self.sendblob(sound_key)

#-------------------------------------------

# This handler creates a file in Cloud Storage using the cloudstorage
# client library and then serves the file back using the Blobstore API.
class CreateAndServeFileHandler(blobstore_handlers.BlobstoreDownloadHandler):

  def get(self):
    # Get the default Cloud Storage Bucket name and create a file name for
    # the object in Cloud Storage.
    bucket = app_identity.get_default_gcs_bucket_name()

    # Cloud Storage file names are in the format /bucket/object.
    filename = '/{}/blobstore_serving_demo'.format(bucket)

    # Create a file in Google Cloud Storage and write something to it.
    with gcs.open(filename, 'w') as filehandle:
      filehandle.write('abcde\n')

    # In order to read the contents of the file using the Blobstore API,
    # you must create a blob_key from the Cloud Storage file name.
    # Blobstore expects the filename to be in the format of:
    # /gs/bucket/object
    blobstore_filename = '/gs{}'.format(filename)
    blob_key = blobstore.create_gs_key(blobstore_filename)

    # BlobstoreDownloadHandler serves the file from Google Cloud Storage to
    # your computer using blob_key.
    self.send_blob(blob_key)


# This datastore model keeps track of which users uploaded which sounds.
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)
  # TODO

class UserSound(ndb.Model):
  user = ndb.StringProperty()
  blob_key = ndb.BlobKeyProperty()
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class SoundUploadFormHandler(webapp2.RequestHandler):
  def get(self):
    # [START upload_url]
    upload_url = blobstore.create_upload_url('/sound/upload/')
    # [END upload_url]
    # [START upload_form]
    # To upload files to the blobstore, the request method must be "POST"
    # and enctype must be set to "multipart/form-data".
    self.response.out.write("""
<html><body>
<h2>Sound Upload</h2>
<form action="{0}" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form>
</body></html>""".format(upload_url))
    # [END upload_form]


# [START ViewSoundHandler]
class ViewSoundHandler(blobstore_handlers.BlobstoreDownloadHandler):
  def get(self, sound_key):
    logging.info(' VIEW SOUND HANDLER: %s' % sound_key)
    if not blobstore.get(sound_key):
      self.error(404)
    else:
      self.send_blob(sound_key)
# [END ViewSoundHandler]

# https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/read-write-to-cloud-storage
class SoundListHandler(webapp2.RequestHandler):
  def get(self):
    bucket_name = os.environ.get('BUCKET_NAME',
                                 app_identity.get_default_gcs_bucket_name())

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Demo GCS Application running from Version: '
                      + os.environ['CURRENT_VERSION_ID'] + '\n')
    self.response.write('Using bucket name: ' + bucket_name + '\n\n')

    self.response.write('Listbucket results:\n')

    bucket = '/' + bucket_name
    page_size = 100
    stats = gcs.listbucket(bucket + '/', max_keys=page_size)
    self.response.write('Stats for #%s entries\n' % stats)
    while True:
      count = 0
      for stat in stats:
        count += 1
        self.response.write('Item #%d' % count)
        self.response.write('\n')
        self.response.write(repr(stat))
        self.response.write('\n')
        self.response.write('Count = %d\n' % count)

      if count != page_size or count == 0:
        self.response.write('Breaking = %d\n' % count)
        break



# Shows all available sound files + keys
class SoundDataViewerHandler(webapp2.RequestHandler):
  def get(self):
    q = UserSound.all()

    for p in q.run():
      self.response.out.write(
          '!!! sound_key=: %s  user = %s.' % (p.blob_key, p.user))

# [END all]


# New on 18-July-2017
class SoundUploadUI(webapp2.RequestHandler):
  def get(self):
    phraseKey = self.request.get('phraseKey', '')
    logging.info('phrasekey = %s' % phraseKey)

    phraseObj = db.get(phraseKey)
    logging.info('phraseObj = %s' % phraseObj)

    # To start, show the phrase info.
    template_values = {
      'language': main.Language,
      'phraseObj': phraseObj,
      'phraseKey': phraseKey,
    }
    path = os.path.join(os.path.dirname(__file__), 'phraseSoundSelector.html')
    self.response.out.write(template.render(path, template_values))
# [END SoundUploadHandler]

# Start the upload to Cloud Storage
class SoundFileUploadHandler(webapp2.RequestHandler):
  def post(self):
    phraseKey = self.request.get('phraseKey', '')
    filename = self.request.get('name', '')
    logging.info('phrasekey = %s' % phraseKey)
    logging.info('filename = %s' % filename)

    phraseObj = db.get(phraseKey)
    logging.info('phraseObj = %s' % phraseObj)

    # Create a Cloud Storage client.
    client = gcs.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # To start, show the phrase info.
    template_values = {
      'language': main.Language,
      'phraseObj': phraseObj,
      'phraseKey': phraseKey,
    }
    path = os.path.join(os.path.dirname(__file__), 'phraseSoundSelector.html')
    self.response.out.write(template.render(path, template_values))
# [END SoundUploadHandler]
SoundFileUploadHandler
