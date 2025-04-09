from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

app = Flask(__name__)

def decrypt_file(encrypted_data, key):
    try:
        # Extract the IV from the beginning of the encrypted data
        iv = encrypted_data[:16]  # Assuming AES block size of 16 bytes
        ciphertext = encrypted_data[16:]

        # Create the cipher object with the key and the extracted IV
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt data (also unpad)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Ensure the file is part of the request
        if 'file' not in request.files:
            return "No file part in the request", 400

        # Receive the uploaded file
        file = request.files['file']
        encrypted_data = file.read()  # Read the encrypted file content
        
        # Replace with the actual encryption key used by the client
        decryption_key = b"thisisaverysecurekey123456789012"  # Must match the client's key
        
        # Decrypt the data
        plaintext = decrypt_file(encrypted_data, decryption_key)
        
        # Ensure the decrypted_files directory exists
        output_dir = "./decrypted_files"
        os.makedirs(output_dir, exist_ok=True)

        # Save the decrypted data to a file, appending if it already exists
        output_file_path = os.path.join(output_dir, "output.txt")
        with open(output_file_path, "ab") as f:  # Open in append mode
            f.write(plaintext)
        
        return "File received and decrypted successfully!", 200
    except Exception as e:
        return f"Error processing file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)