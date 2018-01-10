'''
	search.py

	Given user search query, retrieves relevant twitter data
	Returns descriptive stats for data retrieved
	e.g.

	python search.py Donald Trump
	>
	> Searching twitter for mentions of 'Richard Branson'
	>
	> Results:
	> Tweets returned: 4312
	> Positive: 1234
	> Negative: 2120
	> Neutral: 903

'''
# authenticate/connect
import json
from sys import argv

from twython import Twython
from textblob import TextBlob

from apiKey import API_KEY, API_SECRET

def authenticate(key, secret):
	''' given api key and api secret
	returns access token for twitter api '''
	twitter = Twython(key, secret, oauth_version=2)
	token = twitter.obtain_access_token()
	return token

def search(query, key, token):
	''' given search query, api key, and access token
	returns twitter search results as json object '''
	twitter = Twython(key, access_token=token)
	json = twitter.search(q=query)
	return json

def execute_search(key, secret, query):
	''' given authenticated query
	returns json data '''
	ACCESS_TOKEN = authenticate(key, secret)
	results = search(query, key, ACCESS_TOKEN)
	return results

def parse_json(json_object):
	''' given search results as json object
	parses results into list '''
	print(json.dumps(json_object, sort_keys=True, 
		indent=4, separators=(',', ': ')))

def print_json(json_object):
	tweets = json.load(json_object)
	for tweet in tweets:
		print(tweet['text'])

def print_tweets(results):
	''' given search results object
	prints tweet text each line '''
	for tweet in results['statuses']:
		blob = TextBlob(tweet['text'])
		print('Sentiment: {0}'.format(blob.sentiment.polarity))


'''
    print 'Tweet from @%s Date: %s' % (tweet['user']['screen_nam\
                                       e'].encode('utf-8'),
                                       tweet['created_at'])
    print tweet['text'].encode('utf-8'), '\n'
'''

# collect/parse results
# preprocess text
# sentiment analysis

# sentiment stats

if __name__ == '__main__':
	print('Searching for tweets about: {0}'.format(argv[1]))
	data = execute_search(API_KEY, API_SECRET, argv[1])
	print_tweets(data)