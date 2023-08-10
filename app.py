import sqlite3
from flask import Flask, jsonify, request
import requests
from cachetools import TTLCache

app = Flask(__name__)
cache = TTLCache(maxsize=100, ttl=300)  # Cache user data for 5 minutes

# reterive data from the api, if not present in local database 
def fetch_user_data_from_api(first_name):
    url = f"https://dummyjson.com/users/search?q={first_name}"
    res = requests.get(url)
    fetched_data = res.json()['users']
    users = []
    for data in fetched_data:
        user = {
        'first_name' : data['firstName'], 
        'last_name': data['lastName'],  
        'age' : data['age'],
        'gender' : data['gender'],
        'phone' : data['phone'],
        'email' : data['email'],
        'birth_date' : data['birthDate']
        }
        users.append(user)
    return users

def initialize_database():
    connection = sqlite3.connect('users.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

@app.route('/api/users', methods=['GET'])
def index():
    try:
        first_name = request.args.get('first_name')
        if not first_name:
            return jsonify({"error": "Missing 'first_name' parameter"}), 400

        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row

        query = "SELECT * FROM users WHERE first_name = ?"
        users = conn.execute(query, (first_name,)).fetchall()

        if len(users) == 0:
            if first_name in cache:
                users = cache[first_name]
            else:
                fetched_users = fetch_user_data_from_api(first_name)
                insert_query = "INSERT INTO users (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
                for user in fetched_users:
                    conn.execute(insert_query, (user['first_name'], user['last_name'], user['age'], user['gender'], user['email'], user['phone'], user['birth_date']))

                conn.commit()
                cache[first_name] = fetched_users
                users = fetched_users

        conn.close()

        user_list = [dict(user) for user in users]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    initialize_database()
    app.run()
