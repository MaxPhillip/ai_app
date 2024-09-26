from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from openai import OpenAI

app = Flask(__name__)
app.config['SECRET_KEY'] = '1'

def init_db():
    # a function to intiailise the database and create the users table if it doesn't exist
    conn = sqlite3.connect('ai_flask.db')
    cursor = conn.cursor()
    # cursor.execute is used to execute SQL commands
    # creates a cursor object to interact with the database named basic_flask.db
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS userdata ( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, age INTEGER NOT NULL)''')
    # executes the SQL command to create the users table if it doesn't exist
    conn.commit()
    conn.close()

@app.route('/')
def welcome():
    return render_template('/welcome.html')

@app.route('/login')
def load_login():
    return render_template('/login.html')

@app.route('/register')
def load_register():
    return render_template('/register.html')

@app.route('/home')
def home():
    if 'user' in session:
        user = session['user']
        age = session['age']
        return render_template('home.html', user=user, age=age)
    return redirect(url_for('load_login'))


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username'] #gets the username from the form
    password = request.form['password'] #gets the password from the form
    age = request.form['age'] # gets the age form the form
    conn = sqlite3.connect('ai_flask.db') # connects to the database
    cursor = conn.cursor() #cursor object to interact with the database
    cursor.execute('INSERT INTO userdata (username, password, age) VALUES (?, ?, ?)', (username, password, age))
    conn.commit() #commits the change to the database
    conn.close() # closes the connection to the database
    flash('User registered successfully!', 'success!')
    return redirect(url_for('load_login')) # redirects the user to the login page

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    #using request.form to get the username from the form
    password = request.form['password']
    conn = sqlite3.connect('ai_flask.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM userdata WHERE username = ? AND password = ?', (username, password))
    #? is a placeholder for the values that will be passed in the execute() function
    #(username, password) are the values that will subsitue ? in the execute() function
    # ? is a parameterised query to prevent SQL infection attacks
    user = cursor.fetchone() #fetches the first row of the result
    conn.close()
    if user:
        session['user'] = user[1]
        print(user)
        session['age'] = user[3]
        return redirect(url_for('home'))
    else:
        return redirect(url_for('load_login'))

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)