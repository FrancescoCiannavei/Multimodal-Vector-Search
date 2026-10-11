from os import environ
import psycopg2

def connectDb():
    return psycopg2.connect(
        host = environ["DB_HOST"],
        database = environ["DB_DATABASE"],
        user = environ["DB_USERNAME"],
        password = environ["DB_PASSWORD"],
        port = environ["DB_PORT"]
    )

# TODO: Find a better way to make sure the table exists before we start running SQL
# Maybe we can run it as a migration with docker-compose.yaml
def prepareTable():
	conn = connectDb()
	cur = conn.cursor()
	cur.execute("""
			CREATE TABLE IF NOT EXISTS documents (
				id SERIAL PRIMARY KEY,
				title TEXT,
				content TEXT,
				embedding VECTOR(768)
			);
		""")
	conn.commit()
	cur.close()
	conn.close()

def runSql(sql):
	prepareTable()
	conn = connectDb()
	cur = conn.cursor()
	cur.execute(sql)

	rows = cur.fetchall()
	for row in rows:
		print(f"Title: {row[0]}, Content: {row[1]}, Embedding Dimensions: {row[2]}")
	
	cur.close()
	conn.close()
