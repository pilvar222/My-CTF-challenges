from flask import Flask, render_template, request, redirect, url_for, session, send_file
import hashlib
import sqlite3

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8zxa]/'

conn = sqlite3.connect(':memory:',check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )
''')

# Insert a sample admin user with an MD5-hashed password
admin_password_hash = hashlib.md5('adminpassword'.encode()).hexdigest()
cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', ('admin', admin_password_hash))
conn.commit()


@app.route('/')
def welcome():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    return render_template('index.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        entered_password_hash = hashlib.md5(password.encode()).hexdigest()
        query = 'SELECT * FROM users WHERE username = ? AND hashed_password = ?'
        cursor.execute(query, (username, entered_password_hash))
        user = cursor.fetchone()
        if user:
            session['user'] = username
            return redirect(url_for('welcome'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html', error="")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username == "admin":
            return render_template('register.html', error="You can not register as the admin")
        password = request.form['password']
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        cursor.execute('INSERT INTO users (username, hashed_password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html', error="")

@app.route('/backup.zip')
def backup():
    backup_file_path = './backup.zip'
    return send_file(backup_file_path, as_attachment=True, download_name='backup.zip', mimetype='application/zip')

@app.route("/robots.txt")
def robots():
    return "User-agent: *\nDisallow: /backup.zip"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9004)
