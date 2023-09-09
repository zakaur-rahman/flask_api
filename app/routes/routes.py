from flask import request, jsonify
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from app import app
from app.auth import authenticate, generate_token
from flask_cors import cross_origin

client = MongoClient(app.config['MONGODB_URI'])
db = client.get_database()

@app.route('/api/login', methods=["POST"])
@cross_origin()
def login():

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')


    if not email or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    
    user_collection = db['users']
    app.logger.info(data)
    app.logger.info(user_collection)

    existing_user = user_collection.find_one({'email': email})

    if existing_user:
        if sha256_crypt.verify(password, existing_user['password']):
            token = generate_token(email)
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        hashed_password = sha256_crypt.hash(password)
        new_user = {
            'email': email,
            'password': hashed_password
        }
        user_collection.insert_one(new_user)

        token = generate_token(email)
        return jsonify({'token': token})


@app.route('/api/upload_image', methods=["POST"] )
@cross_origin()
@authenticate
def upload():

    data = request.get_json()
    image_name = data.get('image_name')
    image_url = data.get('image_url')

    image_collection = db['images']

    data = {
        'image_name':image_name,
        'image_url' : image_url
    }

    image_collection.insert_one(data)

    return "Uploaded Successfully!"

@app.route("/api/images")
@authenticate
def get_images():
    collection = db["images"]
    recent_documents = collection.find().sort("_id",-1).limit(1)
    data = [{"image_name": doc["image_name"], "image_url": doc["image_url"]} for doc in recent_documents]
    return jsonify(data)