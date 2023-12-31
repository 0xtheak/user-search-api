# User Search API

This is a Flask-based API that allows users to search for user data stored in an SQLite database. Users can search the stored users data by first name. If a user is not found in the database, then the API can fetch the user data from an external API and insert it into the database for future queries.

## Getting Started

Clone the repository:

    git clone https://github.com/0xtheak/user-search-api.git
    cd user-search-api


Install the required dependencies:

    pip3 install -r requirements.txt

    Run the Flask application:
    python3 app.py

The API will start running locally at http://localhost:5000.
API Endpoints
Search Users

Search for user data based on different parameters.

URL: /api/users

Method: GET

Query Parameters:

    first_name: Search by user's first name (required).

Example Usage:

Search for users with the first name "John":

    GET http://localhost:5000/api/users?first_name=John

If a user with the specified first name is not found in the database, then the API will fetch user data from an external API and insert it into the database for future queries.

Schema

The database schema is defined in the schema.sql file. The users table includes the following columns:

    id (Primary Key)
    first_name
    last_name
    age
    gender
    email
    phone
    birth_date

Notes

    This API demonstrates basic search functionality. You can extend it further to support more advanced searching and filtering options.
    The API uses caching to store recently fetched user data and avoid repeated external API requests.
    Ensure that you have the necessary SQLite library installed and have the schema.sql file with the schema definition for the users table in the same directory as app.py.

License

This project is licensed under the MIT License.