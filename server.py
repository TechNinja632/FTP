from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
import random
import string

app = Flask(__name__)

UPLOAD_FOLDER = "/home/yourfolder/ftp/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = generate_random_string() + '_' + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('file_info'))

@app.route('/file_info')
def file_info():
    directory = app.config['UPLOAD_FOLDER']
    files = os.listdir(directory)
    return render_template('file_info.html', directory=directory, files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            flash(f'File {filename} deleted successfully', 'success')
        else:
            flash(f'File {filename} not found', 'error')
    except Exception as e:
        pass  # Ignore any errors that occur during deletion
    return redirect(url_for('file_info'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = 'your_secret_key'  # Change this to a secure secret key
    app.run(host='0.0.0.0', port=port)
