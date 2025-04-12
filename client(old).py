from user_management import register_user, login_user, reset_password
import os

def encrypt_file(input_file, key): #CAN CHANGE TO OTHER METHOD (TEMP STRUCTURE)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv 
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    return iv + ciphertext

def send_to_server(encrypted_data):
    url = '{address}' 
    files = {'file': ('encrypted_file.enc', encrypted_data)}
    response = requests.post(url, files=files)
    return response.text

def main():
    while True:
        print("\nUser Management System")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Check Logs")
        print("5. File Send")
        print("6. Exit")
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
            """need to be implemented."""
            #1. For admistrator
            #2. For user
            #   2.1 user already logged in -> find username and do insert_log()
            #   2.2 not logged in -> let user log in first.
        
        elif choice == '5':
            key = os.urandom(32) #temp random number need to change
            filepath = input("Enter the path of the file to upload: ")
            if os.path.exists(filepath):
                encrypted_data = encrypt_file(input_file, key)
                response = send_to_server(encrypted_data)
                print("Response from server:", response)
            else:
                print("File does not exist.")

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
