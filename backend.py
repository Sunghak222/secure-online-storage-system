from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

app = Flask(__name__)

def decrypt_file(encrypted_data, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        iv = encrypted_data[:16]  # Assuming AES block size of 16 bytes
        ciphertext = encrypted_data[16:]
        
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
        decryption_key = b"your-32-byte-encryption-key"  # Must match the client's key
        
        # Decrypt the data
        plaintext = decrypt_file(encrypted_data, decryption_key)
        
        # Do something with the decrypted data (e.g., save it, process it)
        with open("./decrypted_files/output.txt", "wb") as f:
            f.write(plaintext)
        
        return "File received and decrypted successfully!", 200
    except Exception as e:
        return f"Error processing file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
