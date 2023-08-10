--create table if the table is not exist in the database
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT ,
    last_name TEXT,
    age INTEGER,
    gender TEXT,
    email TEXT,
    phone INTEGER,
    birth_date DATE NOT NULL
);
