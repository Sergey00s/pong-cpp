import psycopg2




# conn = psycopg2.connect(host="localhost", database="database", user="superuser", password="superuser")

# cur = conn.cursor()


class Database:
	def __init__(self, host, database, user, password):
		self.conn = psycopg2.connect(host=host, database=database, user=user, password=password)
		self.cur = self.conn.cursor()


	def query(self, query, *args):
		self.cur.execute(query, *args)
		return self.cur.fetchall()
	

	def execute(self, query, *args):
		self.cur.execute(query, *args)
		self.conn.commit()

	def executemany(self, query, *args):
		self.cur.executemany(query, *args)
		self.conn.commit()

	def close(self):
		self.conn.close()

	def __del__(self):
		self.conn.close()

	def __repr__(self):
		return f"Database(host={self.conn.host}, database={self.conn.database}, user={self.conn.user}, password={self.conn.password})"

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.conn.close()

