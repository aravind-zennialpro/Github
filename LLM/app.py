from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return jsonify({"message": "Login successful", "token": "abcd1234"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401