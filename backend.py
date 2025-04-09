from flask import Flask, request, send_file
import os

app = Flask(__name__)

# Ensure the directory for storing encrypted files exists
ENCRYPTED_FILES_DIR = "./encrypted_files"
os.makedirs(ENCRYPTED_FILES_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "No file part in the request", 400

        file = request.files['file']
        encrypted_data = file.read()  # Read the encrypted file content

        # Save the encrypted file
        output_file_path = os.path.join(ENCRYPTED_FILES_DIR, file.filename)
        with open(output_file_path, "wb") as f:
            f.write(encrypted_data)

        return "File uploaded successfully!", 200
    except Exception as e:
        return f"Error processing file: {e}", 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        file_path = os.path.join(ENCRYPTED_FILES_DIR, filename)
        if not os.path.exists(file_path):
            return "File not found", 404

        return send_file(file_path)
    except Exception as e:
        return f"Error downloading file: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)