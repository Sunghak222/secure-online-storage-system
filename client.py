from user_management import register_user, login_user, reset_password

def main():
    while True:
        print("\nUser Management System")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(register_user(username, password))

        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(login_user(username, password))

        elif choice == '3':
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            print(reset_password(username, new_password))

        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
