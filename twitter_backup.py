import logging
import pickle
from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import RequestHandler, template
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue
import tweepy

from datetime import datetime
from datetime import timedelta

import config
import helper
from storage import USER
from storage import TWEETS

def get_user():
	st_users = db.GqlQuery("SELECT * FROM USER LIMIT 1")
	if st_users.count() >= 1:
		for user in st_users:
			if user:
				return user
			else:
				return None
	else:
		return None
	
def backup(mode):
	user = get_user()
	if user:
		# authenticate for twitter
		auth = tweepy.OAuthHandler(config.twitter_consumer_token(), config.twitter_consumer_secret())
		auth.set_access_token(user.twitter_oauth_token_key, user.twitter_oauth_token_secret)
		api = tweepy.API(auth)
				
		counter = 1
		last_status = None
						
		statuses = None					
		if mode == 'past':
			statuses = tweepy.Cursor(api.user_timeline, id = user.twitter_username, max_id = user.backedup_last_id, count = helper.number_of_tweets_to_request_per_cycle()).items(helper.number_of_tweets_to_request_per_cycle())
		elif mode == 'present':
			statuses = tweepy.Cursor(api.user_timeline, id = user.twitter_username, since_id = user.backedup_first_id, count = helper.number_of_tweets_to_request_per_cycle()).items(helper.number_of_tweets_to_request_per_cycle())
		
		# iterate over the last status object reveived for the timeline requested
		for status in statuses:
			current_tweet = None
					
			# check if this tweet is already partially written to the db
			if helper.does_tweet_exist(status.id): 
						
				# fetch the already written status object from the db
				tweets = db.GqlQuery("SELECT * FROM TWEETS WHERE tweet_id =:current_tweet_id LIMIT 1", current_tweet_id = status.id)
				if tweets.count() >= 1:
					for tweet in tweets:
						if tweet:
							current_tweet = tweet
				else:
					# if someone else has deleted this entry in the meantime, just create a new one.
					current_tweet = TWEETS()
			else:
				# create a new TWEETS instance because there isn't anything there yet.
				current_tweet = TWEETS()
					
			# save the status to the db
			current_tweet.tweet_id = status.id
			current_tweet.message = status.text
			current_tweet.datetime = status.created_at
			current_tweet.client_used = status.source
			current_tweet.avatar = status.author.profile_image_url
			current_tweet.put()
					
			if counter == helper.number_of_tweets_to_request_per_cycle():
				last_status = status.id
			else:
				counter = counter + 1 # not sure of there's an easier notation
				
		# save the last status_id to the user account in order not to backup the same things multiple times.
		user.backedup_last_id = last_status
		user.put()
		return True
	else:
		logging.error('no user was found in the database, please add one')
		return False

class BackupPresent(webapp.RequestHandler):
	def get(self):
		if backup('present') == False:
			self.error(500)
		else:
			self.response.out.write('backup was successful')
			
class BackupPast(webapp.RequestHandler):
	def get(self):
		if backup('past') == False:
			self.error(500)
		else:
			self.response.out.write('backup was successful')
	