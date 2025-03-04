from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import os
import fitz
import pandas as pd
import logging
import re
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
from core_utils import extract_pdf_data

# App configuration using environment variables for sensitive data
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

# Setup logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# Create a global ThreadPoolExecutor (adjust max_workers as needed)
executor = ThreadPoolExecutor(max_workers=2)

# MongoDB connection using environment variable
mongo_uri = os.environ.get(
    'MONGO_URI',
    "mongodb+srv://dataeng:audywU57R6woeuT5@gaim.m7nzi.mongodb.net/?retryWrites=true&w=majority&tls=true&appName=gaim"
)
client = MongoClient(mongo_uri)
db = client['pdf_csv']  # Database name
collection = db['extracted_text']  # Collection name

# Utility Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def save_to_mongo(data):
    for _, extracted_text in data.items():
        collection.insert_one(extracted_text)

def fetch_all_documents():
    return list(collection.find({}, {'_id': 0}))

# Flask-Login User class
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Background function to process the PDF file
def process_pdf_background(file_path):
    try:
        extracted_text = extract_pdf_data(file_path)
        save_to_mongo(extracted_text)
        logger.info("PDF processed and data saved to MongoDB successfully.")
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == "pdf2csv":
            user = User(user_id=1)
            login_user(user)
            return redirect(url_for('process'))
        else:
            flash('Wrong Username/Password, please try again.', 'error')
            return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/process', methods=['GET'])
@login_required
def process():
    return render_template('process.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'pdf_file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('process'))
    file = request.files['pdf_file']
    if file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('process'))
    if file and allowed_file(file.filename):
        filename = file.filename
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Offload PDF processing to a background thread
        executor.submit(process_pdf_background, file_path)
        flash('File uploaded successfully. Processing in background.', 'success')
        return redirect(url_for('process'))
    else:
        flash('Invalid file format.', 'error')
        return redirect(url_for('process'))

@app.route('/download_csv', methods=['GET'])
@login_required
def download_csv():
    rows = fetch_all_documents()
    if rows:
        df = pd.DataFrame(rows)
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Tasdeed.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        return send_file(csv_path, mimetype='text/csv', as_attachment=True)
    flash('No extracted text found.', 'error')
    return redirect(url_for('process'))

@app.route('/clear_table', methods=['GET'])
@login_required
def clear_table():
    try:
        count = collection.count_documents({})
        if count > 0:
            collection.delete_many({})
            flash('Data cleared successfully.', 'success')
            # Delete all files in UPLOAD_FOLDER
            for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                os.remove(file_path)
        else:
            flash('There is no data to clear.', 'info')
    except Exception as e:
        flash(f'Error clearing data: {str(e)}', 'error')
    return redirect(url_for('process'))

if __name__ == '__main__':
    app.run(debug=True)

