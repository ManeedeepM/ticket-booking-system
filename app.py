from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to something secure in production

# ✅ Initialize the database with users and bookings tables
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    # Bookings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            event TEXT NOT NULL,
            tickets INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()

# ✅ Home page (after login)
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('home.html', username=session['username'])
    return redirect('/login')

# ✅ Register new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "Username already exists. Try another."
        
        conn.close()
        return redirect('/login')
    
    return render_template('register.html')

# ✅ Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/')
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')

# ✅ Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ✅ Booking page
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        event = request.form['event']
        tickets = int(request.form['tickets'])
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO bookings (user_id, name, event, tickets) VALUES (?, ?, ?, ?)',
                  (session['user_id'], name, event, tickets))
        conn.commit()
        conn.close()
        
        return render_template('confirmation.html', name=name, event=event, tickets=tickets)
    
    return render_template('index.html')

# ✅ Run the server
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))  # Railway uses dynamic port
    app.run(debug=True, host='0.0.0.0', port=port)
