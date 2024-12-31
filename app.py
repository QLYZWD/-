from flask import Flask, request, jsonify
from database import Database
import jwt
import os

app = Flask(__name__)
db = Database()
SECRET_KEY = "my_super_secret_key_123"

@app.route('/api/login', methods=['POST'])
def login():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  
  user = db.execute_query(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
  
  if user:
      token = jwt.encode({'user_id': user[0]}, SECRET_KEY, algorithm='HS256')
      return jsonify({'token': token})
  return jsonify({'error': 'Invalid credentials'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
  file = request.files['file']
  filename = file.filename
  file.save(os.path.join('uploads', filename))
  return jsonify({'message': 'File uploaded successfully'})

@app.route('/api/users/<user_id>')
def get_user(user_id):
  user = db.execute_query(f"SELECT * FROM users WHERE id={user_id}")
  return jsonify(user)

if __name__ == '__main__':
  app.run(debug=True)
