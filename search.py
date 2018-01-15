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
from collections import Counter
import json
from sys import argv
import re

from twython import Twython
from textblob import TextBlob

# assumes twitter api key/secret
from apiKey import API_KEY, API_SECRET

#--- Regex parser -----------------------------------------------------------
# source: https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
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

#--- Authenticate & Search ------------------------------------------------------

def authenticate(key, secret):
	''' given twitter api key and secret
	returns access token for api '''
	twitter = Twython(key, secret, oauth_version=2)
	return twitter.obtain_access_token()

def search(query, key, token, num_results):
	''' given search query, api key, and access token
	returns twitter search results as json object '''
	twitter = Twython(key, access_token=token)
	json = twitter.search(q=query, count=num_results)
	return json

def execute_search(key, secret, query, num_results=5):
	''' given authenticated query
	api key, secret, query string, and optional return_count
	returns search results as json object '''
	access_token = authenticate(key, secret)
	results = search(query, key, access_token, num_results)
	return results
 
#--- Processing tweets ------------------------------------------------------------

def tokenize(s):
    return tokens_re.findall(s)

def tokenize2(text):
	'''
	Get all words from text
	'''
	return re.findall('[a-z]+', text.lower())
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# in list of tokenized tweets, split into 2 new lists:
# 1. actual words, and 
# 2. everything else (punctuation marks, RTs, urls, etc)
special_chars = re.compile('[:;,<>.?/\'\"{[_~`!@#$%^&*()]}]')

from string import punctuation

def remove_invalid_str(list_of_tokens):
	''' given tokenized tweet as list of strings
	return list w/ invalid strings removed '''
	invalid_chars = set(punctuation)
	for token in list_of_tokens:
		# if there's a special char in token
		if any(char in invalid_chars for char in token):
			# remove token from list
			list_of_tokens.remove(token)
	return list_of_tokens

def parse_json(json_object):
	''' given search results as json object
	parses results into list '''
	print(json.dumps(json_object, sort_keys=True, 
		indent=4, separators=(',', ': ')))

def print_json(json_object):
	tweets = json.load(json_object)
	for tweet in tweets:
		print(tweet['text'])

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
		print(preprocess(tweet['text']))
		print(' '.join(remove_invalid_str(preprocess(tweet['text']))))
		print('Most common word: ' + most_common(remove_invalid_str(preprocess(tweet['text']))))
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