# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
import main

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

class UserDB(db.Model):
  userName = db.StringProperty(u'')
  userEMail = db.StringProperty(u'')
  userId = db.StringProperty(u'')
  lastUpdate = db.DateTimeProperty(auto_now=True, auto_now_add=True)
  defaultDB = db.StringProperty(u'')
  comment = db.StringProperty('')
  affiliation = db.StringProperty('')


# Return info based on current user.
def getUserInfo(login_target='/', logout_target='/'):
  current_user = users.get_current_user()
  user_nickname = None
  user_logout = None
  user_login = None
  isAdmin = None

  user_login = users.create_login_url(login_target)

  if current_user:
#    logging.info('*** user nickname = %s, email= %s , admin = %s***, id = %s' %
#      (current_user.nickname(), current_user.email(),
#      users.is_current_user_admin(), current_user.user_id()))
    user_logout = users.create_logout_url('/')
    user_nickname = current_user.nickname()
    user_login = users.create_login_url('/words/getWords/')
    isAdmin = users.is_current_user_admin()

#  logging.info('%s, %s, %s, %s' % (current_user, user_nickname, user_logout, user_login))

  return (current_user, user_nickname, user_logout, user_login, isAdmin)


class showUsers(webapp2.RequestHandler): 
  def get(self):
    user_info = getUserInfo(self.request.url)

    q = UserDB.all()
    userCount = 0
    userList = []
    for p in q.run():
      userCount += 1
      userList.append(p)
    self.response.out.write('!!! TODO: %d implement user List.\n' % userCount)
    for v in userList:
      self.response.out.write('\nUser %s, role = %s\n' %
        (v.userEMail, v.userLevel))
 
   #  path = os.path.join(os.path.dirname(__file__), 'userList.html')
   # self.response.out.write(template.render(path, template_values))   


class manageUsers(webapp2.RequestHandler): 
  def get(self):
    #user_info = getUserInfo(self.request.url)

    q = UserDB.all()
    userCount = 0
    userlist = []
    for p in q.run():
      userCount += 1
      userlist.append(p)
 
    roleList = ['Admin', 'Edit', 'View']
    template_values = {
      'userlist': userlist,
      'language': main.Language,
      'roleList': roleList,
    }
    path = os.path.join(os.path.dirname(__file__), 'users.html')
    self.response.out.write(template.render(path, template_values))
   
class addUser(webapp2.RequestHandler): 
  def get(self):
    newUserEmail = self.request.get('userEmail', None)
    userRole = self.request.get('role', None)
    privileges = self.request.GET.getall('privileges')
    name = self.request.get('name', None)
    self.response.out.write('\nArguments = %s' % self.request.arguments())
    self.response.out.write('\nEMail = %s' % newUserEmail)

    q = UserDB.all()
    q.filter('userEMail =', newUserEmail)
    
    p = q.get()  # Get all the matching emails.
    if p:
      self.response.out.write('\n!!!: User %s already in database: %s\n' % (
        p, p.userLevel))
    else:
      newUser = UserDB(userEmail=newUserEmail,
        userName=name,
        userLevel=userRole)
      newUser.put()
      
      self.response.out.write('\n!!!: Added User %s in role %s' % (
        newUserEmail, newUser.userLevel))
      

class clearUsers(webapp2.RequestHandler): 
  def get(self):
    q = UserDB.all()
    numDeleted = 0
    for p in q.run():
      UserDB.delete(p)
      numDeleted += 1
    self.response.out.write('\n%d users deleted' % numDeleted)

