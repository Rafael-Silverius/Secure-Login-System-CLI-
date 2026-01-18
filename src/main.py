from database import init_db
from auth import register_user , login_user
from admin import create_admin


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