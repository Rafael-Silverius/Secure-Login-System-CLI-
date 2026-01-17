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
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
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

#------------- Create Admin -------------
def create_admin():
    username = 'admin'
    password = 'admin123'
    role = 'admin'

    hashed = hash_password(password)

    conn=sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute(
            'INSERT INTO users (username,password,role) VALUES (?, ?, ?)',(username,hashed,role)
        )
        conn.commit()
        print("Admin account created.")
    except sqlite3.IntegrityError:
        print("Admin already exists")
    finally:
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

def user_menu(username):
    while True:
        print(f"\n--- Welcome {username} ---")
        print("1. Change Password")
        print("2. Delete Account")
        print("3. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            update_password(username)
        elif choice == '2':
            delete_account(username)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def update_password(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result=cursor.fetchone();
    stored_password = result[0]

    current_pass = getpass.getpass('Enter current password: ').strip()
    if hash_password(current_pass) != stored_password:
        print("Current password is incorrect")
        conn.close()
        return

    new_pass= getpass.getpass("Enter your new password: ").strip()
    confirm_pass = getpass.getpass("Confirm your new password: ").strip()

    if not new_pass:
        print("Passwords can not be empty")
        conn.close()
        return

    if new_pass!=confirm_pass:
        print("Passwords does not match")
        conn.close()
        return

    hashed_new= hash_password(new_pass)
    cursor.execute("UPDATE users SET password = ? WHERE username = ? ",(hashed_new , username))
    conn.commit()
    conn.close()
    print ("Password updated successfully!")

def delete_account(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result=cursor.fetchone();
    stored_password = result[0]

    
    current_pass = getpass.getpass('Enter your password to proceed with account deletion: ').strip()
    if hash_password(current_pass) != stored_password:
        print("Current password is incorrect")
        conn.close()
        return
    
    confirm = input("Are you sure you want to delete your account? (yes/no): ").lower().strip()
    if confirm != "yes":
        print("Account deletion cancelled.")
        conn.close()
        return
    #delete user
    cursor.execute("DELETE FROM users WHERE username= ?",(username,))
    conn.commit()
    conn.close()

    print("Your account has been permanently deleted.")

#---------- Admin menu --------
def admin_menu():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. View all users")
        print("2. Delete user")
        print("3. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_users()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def view_all_users():
    conn = sqlite3.connect(DB_FILE)
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM users")
    users= cursor.fetchall()
    conn.close()

    print ("\n ---- Registered Users ---- ")
    for user in users:
        print(f"ID: {user[0]} | Username: {user[1]} | Role: {user[3]}")

def delete_user():
    return

# --------- CLI Menu ---------


def main():
    init_db()

    create_admin()
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
