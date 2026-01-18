import getpass
import sqlite3
from database import DB_FILE
from utils import hash_password
from user import user_menu
from admin import admin_menu
from datetime import datetime


# --------- Register User ---------
def register_user():
    username = input("Enter a username: ").strip()
    password = getpass.getpass("Enter a password: ").strip()
    role = 'user'
    
    # TODO: Add validation for empty username/password
    if (not username or not password):
        print ("Username and password are required to register") 
        return;
    
    hashed = hash_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)", (username, hashed, role,datetime.utcnow().isoformat()))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.commit()
        conn.close()


def log_login_attempt(user_id, success):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO login_history (user_id, login_time, success) VALUES (?, ?, ?)",
        (user_id, datetime.utcnow().isoformat(), int(success))
    )

    conn.commit()
    conn.close()

# --------- Login User ---------
def login_user():
    username = input("Enter your username: ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    
    if not username or not password:
        print("Username and password are required to login")
        return 
    
    hashed = hash_password(password)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    

    cursor.execute('SELECT ID, password, role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        user_id , stored_password, role = result
        if hashed == stored_password:
           
            cursor.execute("UPDATE users SET last_login = ? WHERE username = ?", (datetime.utcnow().isoformat(), username))
            conn.commit()
            log_login_attempt(user_id, 1)
            print (f"Login successfully! Welcome, {username}.")

            if role=='admin':
                admin_menu()
            else:
                user_menu(username)
        else:
            print ("Incorrect password.")
            log_login_attempt(user_id , 0)
    else:
        print ("Username not found. Please register first")

    conn.close()
