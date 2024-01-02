from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["user_data"]
collection = db["users"]

@app.route("/api/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

@app.route("/api/get_users", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return jsonify(users)

@app.route("/api/update_user/<name>", methods=["PUT"])
def update_user(name):
    data = request.get_json()
    collection.update_one({"name": name}, {"$set": data})
    return jsonify({"message": f"User {name} updated successfully"})

@app.route("/api/delete_user/<name>", methods=["DELETE"])
def delete_user(name):
    collection.delete_one({"name": name})
    return jsonify({"message": f"User {name} deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
