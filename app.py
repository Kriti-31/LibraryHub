from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "5106cd20b7aed78fefe6234ae818fa1f2a325ce48118738b9932c78b3cc17"
DB_NAME = os.path.join(os.path.dirname(__file__), "database.db")

# ----------------- DATABASE HELPERS -----------------
def init_db():
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_user(fullname, email, password):
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )
            conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Email already registered!")

def check_user(email, password):
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        return cursor.fetchone()

def get_user_by_email(email):
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        return cursor.fetchone()

def update_user_details(user_id, fullname, email, password=None):
    with sqlite3.connect(DB_NAME, timeout=10) as conn:
        cursor = conn.cursor()
        if password:
            cursor.execute(
                "UPDATE users SET fullname=?, email=?, password=? WHERE id=?",
                (fullname, email, password, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET fullname=?, email=? WHERE id=?",
                (fullname, email, user_id)
            )
        conn.commit()

# Initialize database
init_db()

# ----------------- ROUTES -----------------
@app.route('/')
def welcome_page():
    return render_template('welcome.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = ""
    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm-password'].strip()

        if password != confirm_password:
            message = "Passwords do not match!"
        else:
            try:
                add_user(fullname, email, password)
                session['user_email'] = email
                return redirect(url_for('homepage'))
            except ValueError:
                message = "Email already registered!"
    return render_template('signup.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()
        user = check_user(email, password)
        if user:
            session['user_email'] = email
            return redirect(url_for('homepage'))
        else:
            message = "Invalid credentials. Try again."
    return render_template('login.html', message=message)

@app.route('/homepage')
def homepage():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    user = get_user_by_email(session['user_email'])
    user_dict = {"id": user[0], "fullname": user[1], "email": user[2]}
    return render_template('homepage.html', user=user_dict)

@app.route('/dashboarduser', methods=['GET', 'POST'])
def dashboarduser():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    user = get_user_by_email(session['user_email'])
    user_dict = {"id": user[0], "fullname": user[1], "email": user[2]}
    message = ""

    if request.method == 'POST':
        fullname = request.form['fullname'].strip()
        email = request.form['email'].strip().lower()
        current_password = request.form['current-password'].strip()
        new_password = request.form['new-password'].strip()

        if new_password:
            if current_password != user[3]:
                message = "Current password is incorrect!"
            else:
                update_user_details(user[0], fullname, email, password=new_password)
                session['user_email'] = email
                message = "Details updated successfully!"
                user_dict.update({"fullname": fullname, "email": email})
        else:
            update_user_details(user[0], fullname, email)
            session['user_email'] = email
            message = "Details updated successfully!"
            user_dict.update({"fullname": fullname, "email": email})

    return render_template('dashboarduser.html', user=user_dict, message=message)

@app.route('/books')
def books_page():
    return render_template('books.html')

@app.route('/contact')
def get_in_touch_page():
    return render_template('getintouch.html')

@app.route('/contactus')
def contactus_page():
    return render_template('contactus.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))

# ----------------- RUN APP -----------------
if __name__ == '__main__':
    # local ke liye debug
    app.run(debug=True)
