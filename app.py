from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("config/firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)

# Get a book by ID
@app.route("/api/books/<id>", methods=["GET"])
def get_book(id):
    try:
        doc = db.collection("Books").document(id).get()
        if doc.exists:
            book = doc.to_dict()
            book['id'] = doc.id  # Include the ID in the response
            return jsonify(book), 200
        else:
            return jsonify({"Error ": f"Book with id {str(id)} not found"}), 404
    except Exception as e:
        return jsonify({"Error ": str(e)}), 400

# Get all books
@app.route("/api/books", methods=["GET"])
def get_books():
    try:
        books = db.collection("Books").stream()
        books_list = [{**book.to_dict(), "id": book.id} for book in books]
        return jsonify(books_list), 200
    except Exception as e:
        return jsonify({"Error ": str(e)}), 400

# Add a new book
@app.route("/api/books", methods=["POST"])
def add_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error": "no book data is supplied"}), 400
        db.collection("Books").add(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"Error ": str(e)}), 400

# Update a book by ID
@app.route("/api/books/<id>", methods=["PUT"])
def update_book(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        db.collection("Books").document(id).update(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"Error ": str(e)}), 400

# Delete a book by ID
@app.route("/api/books/<id>", methods=["DELETE"])
def delete_book(id):
    try:
        db.collection("Books").document(id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"Error ": str(e)}), 400
