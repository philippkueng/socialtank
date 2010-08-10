from google.appengine.ext import db

class TWEETS(db.Model):
	tweet_id = db.IntegerProperty()
	message = db.StringProperty(multiline=True)
	datetime = db.DateTimeProperty()
	client_used = db.StringProperty(multiline=False)
	avatar = db.StringProperty(multiline=False)	

class USER(db.Model):
	fullname = db.StringProperty()
	twitter_username = db.StringProperty(multiline=False)
	twitter_oauth_token_key = db.StringProperty()
	twitter_oauth_token_secret = db.StringProperty()
	last_saved_tweet = db.ReferenceProperty(TWEETS) # to get the last tweet_id
	
	backedup_last_id = db.IntegerProperty()
	backedup_first_id = db.IntegerProperty()
	
class CONFIG(db.Model):
	make_archive_public = db.BooleanProperty() #check if this can be a boolean type variable