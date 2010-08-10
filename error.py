from google.appengine.ext import webapp

class Error(webapp.RequestHandler):
	def get(self):
		self.response.out.write('there was an error somewhere')