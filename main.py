#!/usr/bin/env python
#
#
# socialtank - backup your tweets on AppEngine
# http://github.com/philippkueng/socialtank
#
# author:
# Philipp, http://philippkueng.ch, http://twitter.com/philippkueng
#
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template
from google.appengine.ext.webapp.util import run_wsgi_app
import os

import sys
sys.path.insert(0, 'tweepy.zip')

import twitter_auth
import twitter_backup
import show_tweets
import error

class MainHandler(webapp.RequestHandler):
    def get(self):
		try:
			values = {}
			path = os.path.join(os.path.dirname(__file__), 'main.htm')
			self.response.out.write(template.render(path, values))
		except:
			self.redirect('/error')

def main():
    application = webapp.WSGIApplication([('/', MainHandler),	
						('/show', show_tweets.Default),
						('/twitter', twitter_auth.Authenticate_for_Twitter),
						('/twitter/callback', twitter_auth.Authenticate_for_Twitter_Callback),
						('/backup/present', twitter_backup.BackupPresent), #only callable from the logic itself
						('/backup/past', twitter_backup.BackupPast), #only callable from the logic itself
						('/error', error.Error),
						('/.*', error.Error404)],
                        debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
