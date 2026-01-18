import getpass
import sqlite3
from database import DB_FILE
from utils import hash_password
from user import user_menu
from admin import admin_menu



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
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
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
    
    # TODO: Check if username exists and password matches
    cursor.execute('SELECT password, role FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()

    if result:
        stored_password, role = result
        if hashed == stored_password:
            print (f"Login successfully! Welcome, {username}.")
            if role=='admin':
                admin_menu()
            else:
                user_menu(username)
        else:
            print ("Incorrect password.")
    else:
        print ("Username not found. Please register first")

    conn.close()
