from flask import Flask, jsonify, request, json
from dotenv import load_dotenv
import os, pymongo
  

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')  

client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db['form_data']

app = Flask(__name__) 

@app.route('/')
def home():
    return "Backend is running"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        form_data = request.get_json()

        name = form_data.get("name")
        age = form_data.get("age")

        collection.insert_one({
            "name": name,
            "age": int(age)
        })

        return jsonify({
            "success": True,
            "message": "Data submitted successfully"
        }), 200

    except pymongo.errors.ServerSelectionTimeoutError:
        return jsonify({
            "success": False,
            "message": "Database not available"
        }), 500

    except Exception:
        return jsonify({
            "success": False,
            "message": "Something went wrong"
        }), 500   

@app.route('/api', methods=['GET'])
def get_data():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/view', methods=['GET'])
def view_data():

    data = collection.find()

    data = list(data)

    for item in data:
        print(item)

        del item['_id']

    data = {
        "data": data
    }
    return data
    

if __name__ == '__main__':
    app.run( port=9000, debug=True)