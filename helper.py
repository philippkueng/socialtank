import re #for get_application_base_url

from google.appengine.ext import db #for does_tweet_exist
from storage import TWEETS 

# INPUT :: http://www.sample.co.uk:8080/folder/file.htm
# OUTPUT :: http://www.sample.co.uk:8080

def get_application_base_url(current_url):
	#regex = '(https?://[-\w\.]+[\:[0-9]{5}]?)'
	regex = '(https?://[-\w\.]+)'
	match = re.search(regex, current_url)
	if match:
		return match.group(1)
	else:
		return None
		
def does_tweet_exist(tweet_id):
	# make a fast search by key to check if the specified tweet already partially exists in the db
	tweets = db.GqlQuery("SELECT __key__ FROM TWEETS WHERE tweet_id =:tw_id LIMIT 1", tw_id = tweet_id)
	if tweets.count() >= 1:
		return True
	return False
	
def number_of_tweets_to_request_per_cycle():
	return 20