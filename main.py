from flask import Flask
import os
import sys
import logging
from database import AppDatabase, GameDatabase

from flask import Response, jsonify, request, abort, make_response


app = Flask(__name__)

db = AppDatabase("localhost", "database", "superuser", "superuser")
gamebase = GameDatabase("localhost", "database", "superuser", "superuser")

@app.route('/')
def index():
	return 'Hello World!'


@app.route('/users')
def users():
	return str(db.get_all_users())


def generate_api(username):
	api_key = os.urandom(16).hex()
	return api_key

@app.route('/register', methods=["POST"])
def register():
	username = request.form["username"]
	password = request.form["password"]
	email = request.form["email"]
	if db.get_user(username):
		abort(404, description="User already exists")
	key = generate_api(username)
	db.create_user(username, password, email, key)
	return jsonify({"api_key": key})


@app.route("/getapi", methods=["POST"])
def getapi():
	username = request.form["username"]
	password = request.form["password"]
	user = db.get_user(username)
	if not user:
		abort(404, description="User does not exist")
	if user[0][2] != password:
		abort(401, description="Incorrect password")
	return jsonify({"api_key": user[0][6]})


@app.route("/deleteuser", methods=["POST"])
def deleteuser():
	username = request.form["username"]
	password = request.form["password"]
	user = db.get_user(username)
	if not user:
		abort(404, description="User does not exist")
	if user[0][2] != password:
		abort(401, description="Incorrect password")
	db.delete_user(username)
	return jsonify({"message": "User deleted"})


@app.route("/newgame", methods=["POST"])
def newgame():
	api_key = request.form["api_key"]
	user = db.get_user_by_api_key(api_key)
	if not user:
		abort(401, description="Invalid API key")
	





if __name__ == '__main__':
	app.run(debug=True)