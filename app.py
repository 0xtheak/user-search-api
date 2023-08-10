import sqlite3
from flask import Flask, jsonify, request
import requests
from cachetools import TTLCache

app = Flask(__name__)
# Cache user data for 5 minutes
cache = TTLCache(maxsize=100, ttl=300)  

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


# initialize database
def initialize_database():
    connection = sqlite3.connect('users.db')
    with open('schema.sql') as f:
        connection.executescript(f.read())
    connection.commit()
    connection.close()

# fetch data from database
def fetch_user_data_from_database(first_name):
    # database connection
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row

    # select user data query
    query = "SELECT * FROM users WHERE first_name LIKE ? "
    # for retreival similar first name
    partial_first_name = f"{first_name}%"
    # execute the sql query
    users = conn.execute(query, (partial_first_name, )).fetchall()

    # close database connection
    conn.close()
    return users;

@app.route('/api/users', methods=['GET'])
def index():
    try:
        first_name = request.args.get('first_name')
        if not first_name:
            return jsonify({"error": "Missing 'first_name' parameter"}), 400

        users = fetch_user_data_from_database(first_name)

        # retrieve data from the api, if not present in localdabase
        if len(users) == 0:
            if first_name in cache:
                users = cache[first_name]
            else:
                fetched_users = fetch_user_data_from_api(first_name)
                
                # if there is not data returned from the api, send this msg to client 
                if len(fetched_users)==0:
                    return jsonify({"msg" : "Data not available for this username"})

                # database connection
                conn = sqlite3.connect('users.db')
                conn.row_factory = sqlite3.Row

                # insert data query
                insert_query = "INSERT INTO users (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
                for user in fetched_users:
                    check_user_query = "SELECT * FROM users WHERE first_name = ?"
                    user_in_database = conn.execute(check_user_query, (user['first_name'],)).fetchall()

                    
                    # insert only those data whose not present in database
                    if len(user_in_database)==0:
                        conn.execute(insert_query, (user['first_name'], user['last_name'], user['age'], user['gender'], user['email'], user['phone'], user['birth_date']))
                        conn.commit()
                
                # close database connection
                conn.close()
                users = fetch_user_data_from_database(first_name)
                # store in the cache
                cache[first_name] = users
            
        
        user_list = [dict(user) for user in users]
        return jsonify(user_list)
    except Exception as e:
        return jsonify({"error": "Internal Serverl Error"})

if __name__ == '__main__':
    # initialize the database
    initialize_database()

    # start the application
    # for development
    # app.run(debug=True, host="0.0.0.0", port="5000")

    # for production
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)