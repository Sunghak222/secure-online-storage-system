from flask import Flask, request, send_file, jsonify
import os
import re

app = Flask(__name__)

# Ensure the directory for storing encrypted files exists
ENCRYPTED_FILES_DIR = "./encrypted_files"
os.makedirs(ENCRYPTED_FILES_DIR, exist_ok=True)

def is_safe_filename(filename):
    # Use a regex to allow only alphanumeric characters, underscores, and dots
    return re.match(r'^[\w\-. ]+$', filename) is not None

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
        # Validate the filename
        if not is_safe_filename(filename):
            return "Invalid filename", 400

        file_path = os.path.join(ENCRYPTED_FILES_DIR, filename)
        if not os.path.exists(file_path):
            return "File not found", 404

        return send_file(file_path)
    except Exception as e:
        return f"Error downloading file: {e}", 500

@app.route('/files', methods=['GET'])
def list_files():
    try:
        files = os.listdir(ENCRYPTED_FILES_DIR)
        return jsonify(files), 200
    except Exception as e:
        return f"Error listing files: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)