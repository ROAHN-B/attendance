from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Load configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

DATABASE = config['database']
LOGIN_ROUTE = config['login_route']
ATTENDANCE_ROUTE = config['attendance_route']
FLASK_DEBUG = config['flask_debug']

# Function to initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        # Create the Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # Create the Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES Users (id)
            )
        ''')
        conn.commit()

# Initialize the database (if not already created)
init_db()

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for login (checking email and password)
@app.route(LOGIN_ROUTE, methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Login successful!', 'user_id': user[0], 'name': user[1]}), 200
        else:
            return jsonify({'error': 'Invalid credentials!'}), 401

# Route to mark attendance
@app.route(ATTENDANCE_ROUTE, methods=['POST'])
def mark_attendance():
    data = request.json
    user_id = data.get('user_id')
    status = data.get('status')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Attendance (user_id, date, time, status)
            VALUES (?, date('now'), time('now'), ?)
        ''', (user_id, status))
        conn.commit()

    return jsonify({'message': 'Attendance marked successfully!'})

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
