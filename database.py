from postgres import Database



class AppDatabase(Database):

	def __init__(self, host, database, user, password):
		super().__init__(host, database, user, password)
		self._create_tables()
		self._create_admin()


	def _create_admin(self):
		if not self.get_user("admin"):
			self.create_user("admin", "admin", "admin", "admin")

	def _create_tables(self):
		self.execute(""" 

			CREATE TABLE IF NOT EXISTS users (
			id SERIAL PRIMARY KEY,
			username VARCHAR(255) UNIQUE NOT NULL,
			password VARCHAR(255) NOT NULL,
			email VARCHAR(255) UNIQUE NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			api_key VARCHAR(255) NOT NULL
		);
	""")
		

	def create_user(self, username, password, email, api_key):
		self.execute("""
			INSERT INTO users (username, password, email, api_key)
			VALUES (%s, %s, %s, %s)
		""", (username, password, email, api_key))

	def get_user(self, username):
		return self.query("""
			SELECT * FROM users WHERE username = %s
		""", (username,))
	
	def get_user_by_email(self, email):
		return self.query("""
			SELECT * FROM users WHERE email = %s
		""", (email,))
	
	def get_user_by_api_key(self, api_key):
		return self.query("""
			SELECT * FROM users WHERE api_key = %s
		""", (api_key,))
	
	def get_user_by_id(self, id):
		return self.query("""
			SELECT * FROM users WHERE id = %s
		""", (id,))
	
	def get_all_users(self):
		return self.query("""
			SELECT * FROM users
		""")
	

	def update_user(self, username, password, email, api_key):
		self.execute("""
			UPDATE users SET password = %s, email = %s, api_key = %s WHERE username = %s
		""", (password, email, api_key, username))

	def delete_user(self, username):
		self.execute("""
			DELETE FROM users WHERE username = %s
		""", (username,))

	def delete_user_by_id(self, id):
		self.execute("""
			DELETE FROM users WHERE id = %s
		""", (id,))

	def delete_user_by_email(self, email):
		self.execute("""
			DELETE FROM users WHERE email = %s
		""", (email,))

	def delete_user_by_api_key(self, api_key):
		self.execute("""
			DELETE FROM users WHERE api_key = %s
		""", (api_key,))

	def delete_all_users(self):
		self.execute("""
			DELETE FROM users
		""")


	
class GameDatabase(Database):
	def __init__(self, host, database, user, password):
		super().__init__(host, database, user, password)
		self._create_tables()

	
	def _create_tables(self):
		self.execute(""" 

			CREATE TABLE IF NOT EXISTS games (
			id SERIAL PRIMARY KEY,
			room VARCHAR(255) NOT NULL,
			player1 VARCHAR(255) NOT NULL,
			player2 VARCHAR(255) NOT NULL,
			player1_score INT NOT NULL,
			player2_score INT NOT NULL,
			created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
			updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP   
			);
	""")
		


	def save_game(self, room, player1, player2, player1_score, player2_score):
		self.execute("""
			INSERT INTO games (room, player1, player2, player1_score, player2_score)
			VALUES (%s, %s, %s, %s, %s)
		""", (room, player1, player2, player1_score, player2_score))

	def get_game(self, room):
		return self.query("""
			SELECT * FROM games WHERE room = %s
		""", (room,))
	
	def get_game_by_id(self, id):
		return self.query("""
			SELECT * FROM games WHERE id = %s
		""", (id,))
	

	def get_all_games(self):
		return self.query("""
			SELECT * FROM games
		""")