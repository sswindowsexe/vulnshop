import sqlite3

def init_db():
    conn = sqlite3.connect('vulnshop.db')
    c = conn.cursor()
    
    # Create Users table with email and role columns
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create Products table
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            description TEXT
        )
    ''')
    
    # Seed Data (Using INSERT OR IGNORE to prevent duplicate errors on multi-runs)
    c.execute("INSERT OR IGNORE INTO users (id, username, password, email, role) VALUES (1, 'admin', 'admin123', 'admin@shop.com', 'admin')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password, email, role) VALUES (2, 'alice', 'pass123', 'alice@email.com', 'user')")
    c.execute("INSERT OR IGNORE INTO products (id, name, price, description) VALUES (1, 'Laptop', 999.99, 'High performance laptop')")
    c.execute("INSERT OR IGNORE INTO products (id, name, price, description) VALUES (2, 'Phone', 499.99, 'Latest smartphone')")
    c.execute("INSERT OR IGNORE INTO products (id, name, price, description) VALUES (3, 'Tablet', 299.99, 'Portable tablet')")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized and seeded successfully!')