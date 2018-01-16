'''
	Functions to create tweet_db,
	and insert records in tweet_db
'''
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
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

def create_table(conn, create_table_sql):
	''' create database table given db connection
	and sql string to create table
	: param conn: database connection
	: param create_table_sql: a CREATE TABLE statement
	: return: 
	'''
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

'''
Mapping tweet attributes (defined by twitter api) to fields in the tweets table:

	do tweets have a unique identifier? -->	id integer PRIMARY KEY,
	tweet['user']['screen_name'] 		-->	user varchar(30) NOT NULL,
	create_date datetime NOT NULL,
	tweet text NOT NULL,
	rt bin NOT NULL

create_tweet_table = '''
CREATE TABLE IF NOT EXISTS tweets (
	id integer PRIMARY KEY,
	user varchar(30) NOT NULL,
	create_date datetime NOT NULL,
	tweet text NOT NULL,
	rt bin NOT NULL
	);'''

if __name__ == '__main__':
    create_connection("C:\\sqlite\db\pythonsqlite.db")

