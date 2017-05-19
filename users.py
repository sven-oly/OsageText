# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import json
import logging
import os
import urllib
import webapp2

from google.appengine.api import users
from google.appengine.ext.webapp import template

# Return info based on current user.
def getUserInfo(login_target='/', logout_target='/'):
  current_user = users.get_current_user()
  user_nickname = None
  user_logout = None
  user_login = None

  user_login = users.create_login_url(login_target)

  if current_user:
    logging.info('*** user nickname = %s, email= %s , admin = %s***, id = %s' %
      (current_user.nickname(), current_user.email(),
      users.is_current_user_admin(), current_user.user_id()))
    user_logout = users.create_logout_url('/')
    user_nickname = current_user.nickname()
    user_login = users.create_login_url('/words/getWords/')

  logging.info('%s, %s, %s, %s' % (current_user, user_nickname, user_logout, user_login))

  return (current_user, user_nickname, user_logout, user_login)   