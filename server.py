from flask import Flask, request, send_from_directory
from flask_cors import CORS  # dd this line
import os
import subprocess

UPLOAD_FOLDER = 'uploads'
AUTH_TOKEN = 'mysecrettoken'  # Change this!

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)  # Enable CORS globally

@app.route('/')
def home():
    return send_from_directory('web', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    token = request.headers.get('Authorization')
    if token != f'Bearer {AUTH_TOKEN}':
        return 'Unauthorized', 403

    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return 'No file uploaded', 400

    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(filepath)

    # ️ Print the file (Windows Notepad)
    subprocess.run(['notepad', '/p', filepath], shell=True)

    return f'File {uploaded_file.filename} uploaded and sent to printer.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
