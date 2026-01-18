import sqlite3
import getpass
from utils import hash_password
from database import DB_FILE

def user_menu(username):
    while True:
        print(f"\n--- Welcome {username} ---")
        print ("1. View Profile")
        print("2. Change Password")
        print("3. Delete Account")
        print("4. Logout")

        choice = input("Choose an option: ").strip()
        if choice =="1":
            view_profile(username)
        elif choice == "2":
            update_password(username)
        elif choice == '3':
            delete_account(username)
            break
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
def view_profile(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role, created_at, last_login FROM users WHERE username = ?",
        (username,)
    )
    result=cursor.fetchone()
    username, role,created_at,last_login = result
    print(f"Username: {username}")
    print(f'Role: {role}')
    print(f"Account created: {created_at} ")
    print(f"Last Login: {last_login}")

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
