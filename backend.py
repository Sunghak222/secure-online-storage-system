from flask import Flask, request, send_file, jsonify
import os
import re
from file_management import FileManager

app = Flask(__name__)

# Ensure the directory for storing encrypted files exists
BASE_DIR = "./encrypted_files"
os.makedirs(BASE_DIR, exist_ok=True)

def is_safe_filename(filename):
    # Use a regex to allow only alphanumeric characters, underscores, and dots
    return re.match(r'^[\w\-. ]+$', filename) is not None

def get_user_directory(username):
    user_dir = os.path.join(BASE_DIR, username)
    os.makedirs(user_dir, exist_ok=True)  # Create user directory if it doesn't exist
    return user_dir

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        username = request.form.get('username')  # Get username from the form data
        if not username:
            return "Username is required", 400

        if 'file' not in request.files:
            return "No file part in the request", 400

        file = request.files['file']
        encrypted_data = file.read()  # Read the encrypted file content

        # Create a directory for the user and save the encrypted file
        user_dir = get_user_directory(username)
        output_file_path = os.path.join(user_dir, file.filename)
        
        with open(output_file_path, "wb") as f:
            f.write(encrypted_data)

        return "File uploaded successfully!", 200
    except Exception as e:
        return f"Error processing file: {e}", 500

@app.route('/download/<username>/<filename>', methods=['GET'])
def download_file(username, filename):
    try:
        # Validate the filename
        if not is_safe_filename(filename):
            return "Invalid filename", 400

        file_manager = FileManager()
        has_permission = file_manager.has_access(username, filename)
        file_manager.close()

        if not has_permission:
            return "Access denied", 403
        
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)
        
        if not os.path.exists(file_path):
            return "File not found", 404

        return send_file(file_path)
    except Exception as e:
        return f"Error downloading file: {e}", 500

@app.route('/files/<username>', methods=['GET'])
def list_files(username):
    try:
        user_dir = get_user_directory(username)

        file_manager = FileManager()
        shared_files = file_manager.get_files_shared_with(username)
        file_manager.close()

        files = os.listdir(user_dir) + shared_files

        return jsonify(files), 200
    except Exception as e:
        return f"Error listing files: {e}", 500

@app.route('/delete/<username>/<filename>', methods=['DELETE'])
def delete_file(username, filename):
    try:
        # Validate the filename
        if not is_safe_filename(filename):
            return "Invalid filename", 400

        file_manager = FileManager()
        #only owner can delete the file
        is_owner = file_manager.is_owner(username, filename)
        file_manager.close()

        if not is_owner:
            return "You do not have permission to delete this file.", 403
        
        user_dir = get_user_directory(username)
        file_path = os.path.join(user_dir, filename)

        if not os.path.exists(file_path):
            return "File not found", 404

        os.remove(file_path)  # Delete the file
        return "File deleted successfully!", 200
    except Exception as e:
        return f"Error deleting file: {e}", 500
    
@app.route('/share', methods=['POST'])
def share_file():
    try:
        owner = request.form.get('owner')
        filename = request.form.get('filename')
        recipient = request.form.get('recipient')

        if not all([owner, filename, recipient]):
            return "Missing parameters", 400

        if not is_safe_filename(filename):
            return "Invalid filename", 400

        owner_dir = get_user_directory(owner)
        file_path = os.path.join(owner_dir, filename)
        if not os.path.exists(file_path):
            return "Unauthorized or file not found", 403

        file_manager = FileManager()
        file_manager.share_file(owner, filename, recipient)
        file_manager.close()

        return "File shared successfully!", 200
    except Exception as e:
        return f"Error sharing file: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
