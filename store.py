'''
	Functions to insert records into tweets table in Twitter.db
'''

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a connection to sqlite db
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def insert_tweet(conn, tweet_tuple):
	"""
	Create single tweet record in the tweets table
	: param conn: database connection
	: param tweet_tuple: tweet tuple
	"""
	sql = '''
	INSERT INTO tweets(id, user, create_date, tweet, favorite, retweet)
	VALUES(?,?,?,?,?,?);
	'''
	cur = conn.cursor()
	cur.execute(sql, tweet_tuple)

tweets = [
	[],
	[],
	[],
]

def insert_multiple_tweets(conn, list_of_tweets):
	"""
	Bulk insert multiple tweets
	: param conn: database connection
	: param list_of_tweets: tweets encapsulated as list of lists
		a list of all tweets, where each tweet contains 6 elements:
		'id', 'user', 'create_date', 'tweet', 'favorite', 'retweet'
	"""
	sql = '''
	INSERT INTO tweets(id, user, create_date, tweet, favorite, retweet)
	VALUES(?,?,?,?,?,?);
	'''
	cur = conn.cursor()
	cur.executemany(sql, list_of_tweets)



# bulk tweet collection - collect tweets as list of lists
# check for and remove duplicates



'''
Mapping tweet attributes 
(defined by twitter api: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets)
to fields in the tweets table:

	tweet['id']						-->		id integer PRIMARY KEY,
	tweet['user']['screen_name'] 	-->		user varchar(50) NOT NULL,
	tweet['created_at']				-->		create_date text NOT NULL,
	tweet['text']					-->		tweet text NOT NULL,
	tweet['favorited']				--> 	favorite integer NULL,
	tweet['retweeted']				--> 	retweet integer NULL
'''

# write function to convert booleans in tweet record to ints

example_tweet = ()

if __name__ == '__main__':

    cnxn = create_connection('Twitter.db')

    insert_tweet(cnxn, example_tweet)

    # commit transaction and close connection
    cnxn.commit()
    cnxn.close()

