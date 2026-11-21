from flask import Flask, request, render_template, session, redirect, url_for, abort
import sqlite3
import secrets

app = Flask(__name__)
app.secret_key = 'supersecret123'

def get_db():
    conn = sqlite3.connect('vulnshop.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# --- VULNERABILITY 1: CROSS-SITE SCRIPTING (XSS) ---
@app.route('/search')
def search():
    query = request.args.get('q', '')
    # Vulnerable: user input passed directly to template without filtering
    return render_template('search.html', query=query)

# --- VULNERABILITY 2: SQL INJECTION (SQLi) ---
@app.route('/products')
def products():
    pid = request.args.get('id', '1')
    conn = get_db()
    try:
        # Vulnerable SQL compilation structure via raw string concatenation
        query = f"SELECT * FROM products WHERE id = {pid}"
        result = conn.execute(query).fetchall()
    except Exception as e:
        # Returning structural errors helps attackers map backend layouts
        return f"Database Error: {str(e)}", 500
    finally:
        conn.close()
    return render_template('products.html', products=result)

# --- VULNERABILITY 3: AUTHENTICATION BYPASS & BROKEN ACCESS CONTROL ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        
        conn = get_db()
        try:
            # Unprotected logical concatenation framework vulnerable to SQLi Bypass
            q = f"SELECT * FROM users WHERE username='{u}' AND password='{p}'"
            print('DEBUG LOGIN QUERY:', q)
            user = conn.execute(q).fetchone()
        except Exception as e:
            return f"Database Error: {str(e)}", 500
        finally:
            conn.close()
            
        if user:
            session['user'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        return 'Invalid login credentials', 401
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form['username']
        p = request.form['password']
        e = request.form['email']
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', (u, p, e, 'user'))
            conn.commit()
        except Exception as err:
            return f"Registration Error: {str(err)}", 400
        finally:
            conn.close()
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    # Broken Authorization: validates identity exists but fails role-level verification
    if 'user' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('admin.html', users=users)

# --- VULNERABILITY 4: CROSS-SITE REQUEST FORGERY (CSRF) ---
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
        
    conn = get_db()
    
    if request.method == 'POST':
        # user_submitted_token = request.form.get('csrf')
        # if not user_submitted_token or user_submitted_token != session.get('csrf_token'):
        #     abort(403)
        new_email = request.form['email']
        # Zero structural multi-part token validations present on this POST action
        conn.execute('UPDATE users SET email=? WHERE username=?', (new_email, session['user']))
        conn.commit()
        conn.close()
        return 'Profile updated successfully via vulnerable endpoint!'
        
    user_data = conn.execute('SELECT * FROM users WHERE username=?', (session['user'],)).fetchone()
    conn.close()
    
    # Generate an anti-CSRF token ONLY to pass it down to the UI for side-by-side demonstration 
    # The POST block above completely ignores validation checks on purpose
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
        
    return render_template('profile.html', user=user_data, token=session['csrf_token'])

if __name__ == '__main__':
    # Insecure setting enabled for demonstration and testing purposes
    app.run(debug=True, host='0.0.0.0', port=5000)
