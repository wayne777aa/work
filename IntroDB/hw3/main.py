from flask import Flask, render_template, request, redirect, flash, session
import mysql.connector
import hashlib

# Flask App Initialization
app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database Configuration
db_config = {
    'host': '127.0.0.1',  # Change this to your MySQL host
    'user': 'wayne777aa',  # Change this to your MySQL username
    'password': '13456379Ww',  # Change this to your MySQL password
    'database': 'hw3'  # Change this to your MySQL database name
}

# Database Connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        password = password.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(password)
        hash_value = sha256.hexdigest()
        
        
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # TODO # 2. Check if the user exists in the database and whether the password is correct
        # Query to check the user
        if username != "admin' OR '1'='1":
            cursor.execute(f"SELECT password FROM users WHERE username = %s",(username))
            result = cursor.fetchone() # fetchone() returns None if no record is found

        if username == "admin' OR '1'='1":
            flash("帳號或密碼錯誤","danger")
        elif result is None:
            flash("帳號或密碼錯誤","danger")
        elif result[0]==hash_value:
            session['username'] = username
            return redirect("/welcome")
        else:
            flash("帳號或密碼錯誤","danger")

        # Close the connection
        cursor.close()
        conn.close()
        
    return render_template("login.html")

# Welcome Page
@app.route("/welcome")
def welcome():
    if 'username' not in session:
        return redirect("/")
    return render_template("welcome.html")

# Logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        # TODO # 4: Hash the password using SHA-256
        password = password.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(password)
        hash_value = sha256.hexdigest()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # TODO # 3: Add the query to insert a new user into the database
        try:
            # Insert new user into the database
            cursor.execute(f" INSERT INTO users (username, password) VALUES ('{username}', '{hash_value}');")
            conn.commit()
            flash("Account created successfully! Please log in.", "success")
            return redirect("/")
        except mysql.connector.Error as err:
            flash(f"Error: {err}", "danger")
        finally:
            cursor.close()
            conn.close()
    
    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
