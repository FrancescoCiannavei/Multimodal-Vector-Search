from os import environ
import psycopg2
from pgvector.psycopg2 import register_vector

def connectDb():
	conn = psycopg2.connect(
		host = environ["DB_HOST"],
		database = environ["DB_DATABASE"],
		user = environ["DB_USERNAME"],
		password = environ["DB_PASSWORD"],
		port = environ["DB_PORT"]
	)
	# Lets numpy arrays be written to and read from VECTOR columns
	register_vector(conn)
	return conn

def runSql(sql, params=None):
	conn = connectDb()
	try:
		# `with conn` commits on success and rolls back on error, but does not close the connection
		with conn, conn.cursor() as cur:
			cur.execute(sql, params)
			return cur.fetchall() if cur.description else None
	finally:
		conn.close()
