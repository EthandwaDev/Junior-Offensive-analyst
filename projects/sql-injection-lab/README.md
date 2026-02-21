# SQL Injection Vulnerability Lab

## Project Overview
This project demonstrates SQL injection vulnerabilities, exploitation techniques, and defensive measures. It showcases practical understanding of how SQL injection attacks work and how to prevent them.

## Objectives
- Understand SQL injection attack vectors
- Demonstrate common exploitation techniques
- Learn proper parameterized query implementation
- Practice vulnerability remediation

## Vulnerability Categories Covered

### 1. Authentication Bypass
**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
result = db.execute(query)
```

**Attack Vector:**
- Input: `admin' --`
- Result: Bypasses password check

**Remediation:**
```python
query = "SELECT * FROM users WHERE username=? AND password=?"
result = db.execute(query, (username, password))
```

### 2. Data Extraction
**Vulnerable Code:**
```python
query = f"SELECT * FROM products WHERE id={product_id}"
```

**Attack Vector:**
- Input: `1 UNION SELECT username, email, password FROM users`
- Result: Extracts sensitive data

**Remediation:**
- Use parameterized queries
- Implement proper input validation
- Apply principle of least privilege to database accounts

### 3. Blind SQL Injection
**Vulnerable Code:**
```python
query = f"SELECT * FROM users WHERE email='{email}'"
# No feedback, but query executes
```

**Attack Vector:**
- Input: `test@test.com' AND 1=1 --`
- Input: `test@test.com' AND 1=2 --`
- Analyze response differences to extract data

**Remediation:**
- Use prepared statements
- Validate input length and format
- Implement rate limiting

## Defense Strategies

### 1. Parameterized Queries (Prepared Statements)
```python
# Safe approach
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### 2. Input Validation
- Whitelist acceptable characters
- Validate data type and length
- Use allowlist rather than blocklist

### 3. Least Privilege Principle
```sql
-- Create database user with minimal permissions
CREATE USER readonlyuser IDENTIFIED BY 'password';
GRANT SELECT ON database.* TO readonlyuser;
```

### 4. Web Application Firewall (WAF)
- Detect common SQL injection patterns
- Implement rate limiting
- Log suspicious activities

### 5. Output Encoding
- Remove sensitive data from error messages
- Don't display database errors to users

## Tools & Technologies
- **Languages**: Python, SQL
- **Databases**: SQLite, MySQL
- **Testing Tools**: SQLmap, Burp Suite
- **Frameworks**: Flask

## Testing Methodology

### Manual Testing
1. Test input fields with SQL metacharacters: `' " ; --`
2. Attempt UNION-based injection
3. Test blind injection with time delays
4. Analyze error messages for information leakage

### Automated Testing
```bash
sqlmap -u "http://target.com/product?id=1" --dbs
sqlmap -u "http://target.com/login" -data "username=admin&password=test" --forms
```

## Key Takeaways
- **Never trust user input** - Always validate and sanitize
- **Use parameterized queries** - The primary defense against SQL injection
- **Principle of least privilege** - Limit database user permissions
- **Error handling** - Don't expose database errors to users
- **Security testing** - Regularly audit application code

## References
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection)

## Last Updated
February 2026
