from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template
from google.appengine.ext import db

class Default(webapp.RequestHandler):
	def get(self):
		self.response.out.write('hi there, you have ')
		tweets = db.GqlQuery("SELECT __key__ FROM TWEETS")
		self.response.out.write('<strong>' + str(tweets.count()) + '</strong> tweets saved in socialtank.')