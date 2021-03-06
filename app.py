from flask import Flask, request, jsonify, url_for, redirect
from functools import wraps

import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

db = []

cred = credentials.Certificate('firebase_private_key.json')
firebase_app = firebase_admin.initialize_app(cred)

# This function is a decorator
def auth_required(f):
	@wraps(f)
	def verify_token(*args, **kwargs):
		# Verify firebase auth token here
		try:	
			id_token = request.args.get('token')
			result = auth.verify_id_token(id_token)
			print(result['name'] + " made a request")
			return f(user_id=result['uid'], *args, **kwargs)
		except:
			return jsonify({"error": "Bad token"})		
	return verify_token

@app.route("/")
def hello():
    return "RUMAD Accelerator Sample Project Backend"

@app.route("/login")
def login():
    return "login"

@app.route('/transactions', methods=['GET', 'POST'])
@auth_required
def transactions(**kwargs):
	print("the user sending the request is " + str(kwargs['user_id'])) # user_id comes from the variable we passed in the function above
	# MAKE SURE THE @auth_required IS UNDERNEATH THE @app.route
	if request.method == 'POST':
		transaction={
			"type": request.args.get('type'),
			"category": request.args.get('category'),
			"amount": request.args.get('amount')
		}
		db.append(transaction.copy())
		return "SUCCESS"
	else:
		return jsonify(db)



