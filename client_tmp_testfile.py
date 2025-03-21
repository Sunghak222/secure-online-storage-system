import os
from user_management import login_user, reset_password, get_user_role,register_user
from log_management import LogManagement
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_file(input_file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    return iv + ciphertext

def send_to_server(encrypted_data):
    url = '{address}'  # 서버 주소
    files = {'file': ('encrypted_file.enc', encrypted_data)}
    print(encrypted_data)
    # response = requests.post(url, files=files)
    # return response.text

def main():
    is_logged_in = False
    username = ''
    is_admin = False  # 관리자 여부 초기화

    while True:
        print("\nUser Management System")
        if not is_logged_in:
            print("1. Login")
        else:
            print("2. Reset Password")
            if is_admin:  # 관리자일 때만 로그 확인 옵션 표시
                print("3. Check Logs")
                print("4. Register")
            print("5. File Send")
                
        
        print("6. Exit")
        choice = input("Choose an option: ")

        if not is_logged_in and choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = login_user(username, password)
            if response == "Login successful.":
                is_logged_in = True
                
                is_admin = get_user_role(username) == 'administrator'
                print(response)
            else:
                print("Login failed. Please try again.")

        elif is_logged_in and choice == '2':
            new_password = input("Enter new password: ")
            print(reset_password(username, new_password))

        elif is_logged_in and is_admin and choice == '3':
            log_manager = LogManagement()
            username = "administrator" 
            logs = log_manager.get_log(username)
            if logs:
                for log in logs:
                    print(log)
            else:
                print("No logs found for this user.")
            log_manager.close()

        elif is_logged_in and choice == '5':
            key = os.urandom(32)  # tmp random key
            filepath = input("Enter the path of the file to upload: ")
            if os.path.exists(filepath):
                encrypted_data = encrypt_file(filepath, key)
                response = send_to_server(encrypted_data)
                print("Response from server:", response)
            else:
                print("File does not exist.")

        elif choice == '4':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(register_user(username, password))

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()