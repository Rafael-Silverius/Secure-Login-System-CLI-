import sqlite3
from utils import hash_password
from database import DB_FILE
from datetime import datetime

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
            'INSERT INTO users (username,password,role,created_at) VALUES (?, ?, ?, ?)',(username,hashed,role,datetime.utcnow().isoformat())
        )
        conn.commit()
        print("Admin account created.")
    except sqlite3.IntegrityError:
        print("Admin already exists")
    finally:
        conn.close()

#---------- Admin menu --------
def admin_menu():
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. View all users")
        print("2. View Login Attempts")
        print("3. Delete user")
        print("4. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_users()
        elif choice=="2":
            view_login_attempts()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def view_all_users():
    conn = sqlite3.connect(DB_FILE)
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM users")
    users= cursor.fetchall()
    conn.close()

    if not users:
        print ("There are no registered users at the moment")
        return
    

    print ("\n ---- Registered Users ---- ")
    for user in users:
        print(f"ID: {user[0]} | Username: {user[1]} | Role: {user[3]}")

def delete_user():
    view_all_users()
    
    try:
        user_id = int (input("Enter the ID of the account you want to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor= conn.cursor()
    
    cursor.execute("SELECT username, role FROM users WHERE id=?",(user_id,))
    user=cursor.fetchone()
    
    
    if not user:
        print ("User ID does not exist")
        return
    
    username,role = user 

    if role=='admin':
        print("You are not allowed to delete an admin account")
        conn.close()
        return

    confirm = input(f"Are you sure you want to delete user '{username}' (ID: {user_id})? (yes/no)").lower().strip()
    
    if confirm != "yes":
        print("Account deletion cancelled.")
        conn.close()
        return
    
    #delete user
    cursor.execute("DELETE FROM users WHERE ID= ?",(user_id,))
    conn.commit()
    conn.close()
    
    print(f"User '{username}' has been deleted successfully.")

def view_login_attempts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Join users table to show username
    cursor.execute("""
        SELECT lh.id, u.username, lh.login_time, lh.success
        FROM login_history lh
        JOIN users u ON lh.user_id = u.id
        ORDER BY lh.login_time DESC
    """)
    attempts = cursor.fetchall()
    conn.close()

    if not attempts:
        print("\nNo login attempts recorded yet.")
        return

    print("\n--- Login Attempts ---")
    for attempt in attempts:
        attempt_id, username, login_date, success = attempt
        status = "SUCCESS" if success == 1 else "FAILED"
        print(f"ID: {attempt_id} | User: {username} | Date: {login_date} | Status: {status}")