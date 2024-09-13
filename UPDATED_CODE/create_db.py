import sqlite3
import bcrypt

# Create a database and a table to store hashed passwords
def setup_database():
    conn = sqlite3.connect('chat_server.db')
    c = conn.cursor()
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            hashed_password TEXT NOT NULL
        )
    ''')
    # Generate a salt and hash the password
    password = b'password'  # Example password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    # Insert the hashed password into the database
    c.execute('INSERT INTO passwords (hashed_password) VALUES (?)', (hashed_password,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")

