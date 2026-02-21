"""
VULNERABLE APPLICATION - FOR EDUCATIONAL PURPOSES ONLY
This demonstrates SQL injection vulnerabilities that should NEVER be used in production.
"""

import sqlite3
from flask import Flask, render_template, request # type: ignore
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    cursor.execute('''CREATE TABLE products
                     (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT)''')
    
    # Insert sample data
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'password123', 'admin@example.com')")
    cursor.execute("INSERT INTO users VALUES (2, 'user1', 'secret', 'user1@example.com')")
    cursor.execute("INSERT INTO products VALUES (1, 'Widget', 9.99, 'A useful widget')")
    
    conn.commit()
    return conn

conn = init_db()

@app.route('/')
def home():
    return '''
    <h1>SQL Injection Lab - Vulnerable Application</h1>
    <ul>
        <li><a href="/login">Login (Vulnerable)</a></li>
        <li><a href="/products?id=1">Products (Vulnerable)</a></li>
        <li><a href="/search">Search (Vulnerable)</a></li>
    </ul>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # VULNERABLE: String concatenation in SQL query
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                return f"<h2>Welcome {username}!</h2><p>User ID: {user[0]}</p>"
            else:
                return "<h2>Login failed</h2>"
        except Exception as e:
            return f"<h2>Error</h2><pre>{str(e)}</pre>"
    
    return '''
    <h1>Login (Vulnerable to SQL Injection)</h1>
    <form method="POST">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    <p>Try: <code>admin' --</code> as username (no password needed)</p>
    '''

@app.route('/products')
def products():
    product_id = request.args.get('id')
    
    # VULNERABLE: String concatenation in SQL query
    query = f"SELECT * FROM products WHERE id={product_id}"
    
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        
        if result:
            return f"<h2>Product</h2><p>{result[0]}</p>"
        else:
            return "<h2>Product not found</h2>"
    except Exception as e:
        return f"<h2>Error</h2><pre>{str(e)}</pre>"

@app.route('/search')
def search():
    if request.method == 'POST':
        search_term = request.form.get('q')
        
        # VULNERABLE: String concatenation in SQL query
        query = f"SELECT * FROM users WHERE email LIKE '%{search_term}%'"
        
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            
            output = "<h2>Search Results</h2>"
            for row in results:
                output += f"<p>{row}</p>"
            return output
        except Exception as e:
            return f"<h2>Error</h2><pre>{str(e)}</pre>"
    
    return '''
    <h1>Search</h1>
    <form method="POST">
        <input type="text" name="q" placeholder="Search emails">
        <input type="submit" value="Search">
    </form>
    '''

if __name__ == '__main__':
    print("⚠️  This is a VULNERABLE application for educational purposes only!")
    print("DO NOT use this in production or on live systems!")
    app.run(debug=True, port=5000)
