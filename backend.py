from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

app = Flask(__name__)

def decrypt_file(encrypted_data, key):
    try:
        iv = encrypted_data[:16] 
        ciphertext = encrypted_data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "No file part in the request", 400
        file = request.files['file']
        encrypted_data = file.read()  
        
        decryption_key = b"thisisaverysecurekey123456789012"  # need to consider how to not hard coding this key!!!!
        
        plaintext = decrypt_file(encrypted_data, decryption_key)
        
        output_dir = "./decrypted_files"
        os.makedirs(output_dir, exist_ok=True)

        original_filename = file.filename  
        output_filename = f"{original_filename}"  
        
        output_file_path = os.path.join(output_dir, output_filename)
        
        with open(output_file_path, "wb") as f:
            f.write(plaintext)
        
        return f"File received and decrypted successfully! Saved as {output_filename}", 200
    except Exception as e:
        return f"Error processing file: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)