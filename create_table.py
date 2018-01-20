'''
	Functions to create Twitter.db,
	and create tweets table
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
		c.commit()
	except Error as e:
		print(e)


create_tweets_table = '''
CREATE TABLE IF NOT EXISTS tweets (
	id integer PRIMARY KEY,
	user varchar(50) NOT NULL,
	create_date text NOT NULL,
	tweet text NOT NULL,
	favorite integer NULL,
	retweet integer NULL
	);'''

if __name__ == '__main__':
    cnxn = create_connection('Twitter.db')
    create_table(cnxn, create_tweets_table)
    cnxn.close()

