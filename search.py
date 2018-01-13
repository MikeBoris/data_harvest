'''
	search.py

	Given user search query, retrieves relevant twitter data
	Returns descriptive stats for data retrieved
	e.g.

	python search.py 'Richard Branson'
	>
	> Searching twitter for mentions of Richard Branson
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
	json = twitter.search(q=query, count=2)
	return json

def execute_search(key, secret, query):
	''' given authenticated query
	returns json data '''
	ACCESS_TOKEN = authenticate(key, secret)
	results = search(query, key, ACCESS_TOKEN)
	return results

import re
 
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens
 
# tweet = 'RT @marcobonzanini: just an example! :D http://example.com #NLP'
# print(preprocess(tweet))
# ['RT', '@marcobonzanini', ':', 'just', 'an', 'example', '!', ':D', 'http://example.com', '#NLP']

def parse_json(json_object):
	''' given search results as json object
	parses results into list '''
	print(json.dumps(json_object, sort_keys=True, 
		indent=4, separators=(',', ': ')))

def print_json(json_object):
	tweets = json.load(json_object)
	for tweet in tweets:
		print(tweet['text'])

from collections import Counter

def most_common(lst):
	data = Counter(lst)
	return data.most_common(1)[0][0]


def print_tweets(results):
	''' given search results object
	prints tweet text each line '''
	for tweet in results['statuses']:
		print('\n')
		print('==================================')
		print('Screen_name: ' + tweet['user']['screen_name'])
		#print('Created_at: ' + tweet['created_at'])
		print(tweet['text'] + '\n')
		print('Most common word: ' + most_common(preprocess(tweet['text'])))
		#print('Favorite_count: {}'.format(tweet['favorited']))
		#print('Retweet_count: {}'.format(tweet['retweeted']))
		#print('Lang: ' + tweet['lang'])
		#print('Entities: {}'.format(tweet['entities']))

		#blob = TextBlob(tweet['text'])
		#print('Sentiment: {0}'.format(blob.sentiment.polarity))


'''
    print 'Tweet from @%s Date: %s' % (tweet['user']['screen_nam\
                                       e'].encode('utf-8'),
                                       tweet['created_at'])
    print tweet['text'].encode('utf-8'), '\n'

    key attributes of a tweet:

    text: the text of the tweet itself
	created_at: the date of creation
	favorite_count, retweet_count: the number of favourites and retweets
	favorited, retweeted: boolean stating whether the authenticated user (you) have favourited or retweeted this tweet
	lang: acronym for the language (e.g. “en” for english)
	id: the tweet identifier
	place, coordinates, geo: geo-location information if available
	user: the author’s full profile
	entities: list of entities like URLs, @-mentions, hashtags and symbols
	in_reply_to_user_id: user identifier if the tweet is a reply to a specific user
	in_reply_to_status_id: status identifier id the tweet is a reply to a specific status
'''

# collect/parse results
# preprocess text
# sentiment analysis

# sentiment stats

if __name__ == '__main__':
	print('Searching for tweets about: {0}'.format(argv[1]))
	data = execute_search(API_KEY, API_SECRET, argv[1])
	print_tweets(data)