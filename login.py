import sqlite3
import hashlib
import os
import getpass

DB_FILE = "users.db"

# --------- Database Setup ---------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# --------- Hashing Function ---------
def hash_password(password):
    """
    Returns a SHA-256 hash of the password
    """
    return hashlib.sha256(password.encode()).hexdigest()

# --------- Register User ---------
def register_user():
    username = input("Enter a username: ").strip()
    password = getpass.getpass("Enter a password: ").strip()
    
    # TODO: Add validation for empty username/password
    
    hashed = hash_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # TODO: Insert new user into DB
        pass
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.commit()
        conn.close()

# --------- Login User ---------
def login_user():
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    
    hashed = hash_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # TODO: Check if username exists and password matches
    pass

    conn.close()

# --------- CLI Menu ---------
def main():
    init_db()
    
    while True:
        print("\n--- Secure Login System ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
