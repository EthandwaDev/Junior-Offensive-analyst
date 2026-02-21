"""
SECURE APPLICATION - SQL Injection Prevention
Demonstrates proper implementation using parameterized queries.
"""

import sqlite3
from flask import Flask, render_template, request
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE users
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    
    cursor.execute('''CREATE TABLE products
                     (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT)''')
    
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'hashed_pwd_admin', 'admin@example.com')")
    cursor.execute("INSERT INTO users VALUES (2, 'user1', 'hashed_pwd_user1', 'user1@example.com')")
    cursor.execute("INSERT INTO products VALUES (1, 'Widget', 9.99, 'A useful widget')")
    
    conn.commit()
    return conn

conn = init_db()

def validate_username(username):
    """Validate username format"""
    if not username or len(username) > 50:
        return False
    if not re.match(r'^[a-zA-Z0-9_.-]+$', username):
        return False
    return True

@app.route('/')
def home():
    return '''
    <h1>SQL Injection Prevention - Secure Application</h1>
    <ul>
        <li><a href="/login">Secure Login</a></li>
        <li><a href="/products?id=1">Secure Products</a></li>
        <li><a href="/search">Secure Search</a></li>
    </ul>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Input validation
        if not validate_username(username):
            return "<h2>Invalid username format</h2>"
        
        if not password or len(password) > 255:
            return "<h2>Invalid password</h2>"
        
        # SECURE: Parameterized query using ?
        query = "SELECT * FROM users WHERE username=? AND password=?"
        
        cursor = conn.cursor()
        try:
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                return f"<h2>Login successful</h2><p>Welcome {username}! (ID: {user[0]})</p>"
            else:
                return "<h2>Login failed - Invalid credentials</h2>"
        except Exception as e:
            return "<h2>An error occurred</h2>"
    
    return '''
    <h1>Secure Login</h1>
    <form method="POST">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    <p>Use: admin / hashed_pwd_admin</p>
    <p><strong>Protected against SQL injection:</strong></p>
    <ul>
        <li>Parameterized queries only</li>
        <li>Input validation on username</li>
        <li>Length restrictions</li>
        <li>No error details exposed to user</li>
    </ul>
    '''

@app.route('/products')
def products():
    product_id = request.args.get('id', '')
    
    # Input validation
    try:
        product_id = int(product_id)
        if product_id <= 0:
            return "<h2>Invalid product ID</h2>"
    except ValueError:
        return "<h2>Product ID must be a number</h2>"
    
    # SECURE: Parameterized query
    query = "SELECT * FROM products WHERE id=?"
    
    cursor = conn.cursor()
    try:
        cursor.execute(query, (product_id,))
        result = cursor.fetchone()
        
        if result:
            return f"<h2>Product</h2><p>ID: {result[0]}, Name: {result[1]}, Price: ${result[2]}</p>"
        else:
            return "<h2>Product not found</h2>"
    except Exception as e:
        return "<h2>An error occurred</h2>"

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('q', '')
        
        # Input validation
        if not search_term or len(search_term) > 100:
            return "<h2>Invalid search term</h2>"
        
        # SECURE: Parameterized query
        # Note: LIKE requires wildcards to be added safely
        search_pattern = f"%{search_term}%"
        query = "SELECT id, email FROM users WHERE email LIKE ?"
        
        cursor = conn.cursor()
        try:
            cursor.execute(query, (search_pattern,))
            results = cursor.fetchall()
            
            output = f"<h2>Search Results ({len(results)} found)</h2>"
            if results:
                for row in results:
                    output += f"<p>ID: {row[0]}, Email: {row[1]}</p>"
            else:
                output += "<p>No results found</p>"
            return output
        except Exception as e:
            return "<h2>An error occurred</h2>"
    
    return '''
    <h1>Secure Search</h1>
    <form method="POST">
        <input type="text" name="q" placeholder="Search emails" required>
        <input type="submit" value="Search">
    </form>
    <p><strong>Protected against SQL injection:</strong></p>
    <ul>
        <li>Parameterized LIKE query</li>
        <li>Input length validation</li>
        <li>Safe wildcard handling</li>
        <li>Only non-sensitive data returned</li>
    </ul>
    '''

if __name__ == '__main__':
    print("Running SECURE application with SQL injection prevention!")
    app.run(debug=True, port=5001)
