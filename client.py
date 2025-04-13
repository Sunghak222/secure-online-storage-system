import os
from user_management import login_user, reset_password, register_user
from user_utils import get_user_role, get_user_secret
from log_management import LogManagement
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import requests
import pyotp

# Define a fixed 32-byte key (for testing purposes)
AES_KEY = os.urandom(32)  # Securely generate a random key for each session

def encrypt_file(input_file):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    iv = cipher.iv
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    
    # Return the IV concatenated with the ciphertext
    return iv + ciphertext

def decrypt_file(encrypted_data):
    iv = encrypted_data[:16]  # Extract the IV
    ciphertext = encrypted_data[16:]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def send_to_server(encrypted_data, original_filename, username):
    url = 'http://127.0.0.1:5000/upload'
    files = {'file': (f"{original_filename}.enc", encrypted_data)}
    data = {'username': username}  # Include the username in the request
    response = requests.post(url, files=files, data=data)
    return response.text

def download_file(username, filename):
    url = f'http://127.0.0.1:5000/download/{username}/{filename}'
    response = requests.get(url)
    if response.status_code == 200:
        encrypted_data = response.content
        decrypted_data = decrypt_file(encrypted_data)
        return decrypted_data
    else:
        print("Error downloading file:", response.text)

def list_files(username):
    url = f'http://127.0.0.1:5000/files/{username}'  # Include username in the URL
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of filenames
    else:
        print("Error retrieving file list:", response.text)
        return []

def delete_file(username):
    filename = input("Enter the name of the file to delete: ")
    url = f'http://127.0.0.1:5000/delete/{username}/{filename}'
    response = requests.delete(url)
    if response.status_code == 200:
        print(response.text)
        return response.status_code
    else:
        print("Error deleting file:", response.text)
        return response.status_code

def main():
    is_logged_in = False
    username = ''
    is_admin = False  

    while True:
        # Initialize log manager
        log_manager = LogManagement()
        
        print("\nUser Management System")
        if not is_logged_in:
            print("1. Login")
        else:
            print("2. Reset Password")
            if is_admin:
                print("3. Check Logs")
                print("4. Register")
            print("5. Upload File")
            print("6. Download File")
            print("7. Delete File")  # Add option for deleting files
                
        print("8. Exit")
        choice = input("Choose an option: ")

        if not is_logged_in and choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            response = login_user(username, password)
            if response == "Login successful.":
                # OTP verification
                user_secret = get_user_secret(username)
                user_otp = input("Enter the 6-digit OTP from your Authenticator app: ")

                totp = pyotp.TOTP(user_secret)

                # Verify OTP
                if totp.verify(user_otp):
                    is_logged_in = True
                    is_admin = get_user_role(username) == 'administrator'
                    log_manager.insert_log(username, "LOGIN", "Successful log in")
                    print(response)
                else:
                    is_logged_in = False
                    log_manager.insert_log(username, "INVALID_OTP", "Invalid OTP")
                    print("Wrong OTP Number")
            else:
                log_manager.insert_log(username, "INVALID_LOGIN", "Invalid log in")
                print("Login failed. Please try again.")

        elif is_logged_in and choice == '2':
            new_password = input("Enter new password: ")

            user_secret = get_user_secret(username)
            user_otp = input("Enter the 6-digit OTP from your Authenticator app: ")

            totp = pyotp.TOTP(user_secret)
            if totp.verify(user_otp):
                print(reset_password(username, new_password))
                log_manager.insert_log(username, "CHANGE", "Password changed successfully.")
            else:
                print("Invalid OTP. Password reset rejected.")
                log_manager.insert_log(username, "FAILED_CHANGE", "Password reset failed due to invalid OTP.")

        elif is_logged_in and is_admin and choice == '3':
            logs = log_manager.get_log(username)
            if logs:
                print("(ID, TIMESTAMP, USERNAME, ACTION, CONTENT)")
                for log in logs:
                    print(log)
            else:
                print("No logs found for this user.")

        elif is_logged_in and choice == '5':
            filepath = input("Enter the path of the file to upload: ")
            if os.path.exists(filepath):
                encrypted_data = encrypt_file(filepath)
                original_filename = os.path.basename(filepath)  # Get the original filename
                response = send_to_server(encrypted_data, original_filename, username)  # Pass username
                print("Response from server:", response)
                log_manager.insert_log(username, "UPLOAD", "File uploaded.")
            else:
                print("File does not exist.")
                log_manager.insert_log(username, "UPLOAD_FAIL", "File cannot be uploaded.")

        elif is_logged_in and choice == '6':
            print("Available files for download:")
            files = list_files(username)  # Pass username
            for file in files:
                print(file)

            filename = input("Enter the name of the file to download (with .enc extension): ")
            if filename in files:
                decrypted_data = download_file(username, filename)  # Pass username
                if decrypted_data:
                    download_dir = "./Download"
                    os.makedirs(download_dir, exist_ok=True)  # Create Download directory if it doesn't exist
                    with open(os.path.join(download_dir, f"decrypted_{filename[:-4]}"), "wb") as f:
                        f.write(decrypted_data)
                    print(f"File downloaded and decrypted as {os.path.join(download_dir, f'decrypted_{filename[:-4]}')}")
                    log_manager.insert_log(username, "DOWNLOAD", "File downloaded.")
            else:
                print("File not found on the server.")

        elif is_logged_in and choice == '7':
            response = delete_file(username)  # Call the delete function
            if (response == 200):
                log_manager.insert_log(username, "DELETE", "file deleted")
            else:
                log_manager.insert_log(username, "DELETE_FAILED", "deletion failed")

        elif choice == '8':
            print("Exiting...")
            log_manager.insert_log(username, "LOGOUT", "User log out")
            break
        
        elif is_logged_in and choice == '4':
            username = input("Enter username: ")
            password = input("Enter password: ")
            print(register_user(username, password))

        else:
            print("Invalid choice. Please try again.")
        log_manager.close()

if __name__ == "__main__":
    main()
