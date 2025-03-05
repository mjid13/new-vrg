from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import os
import unicodedata
import fitz
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import logging
from core_utils import extract_pdf_data
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig()
logger = logging.getLogger(__name__)




# Create a connection to the PostgreSQL database
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataeng:audywU57R6woeuT5@gaim.m7nzi.mongodb.net/?retryWrites=true&w=majority&tls=true&appName=gaim"
)
db = client['pdf_csv']  # Your database name
collection = db['extracted_text']  # Your collection name

import re

def split_string(string):

  pattern = r"-"
  matches = re.finditer(pattern, string)
  last_index = len(string)
  for match in matches:
    last_index = match.start()
  return string[last_index:]

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    # Load the user from the user_id
    return User(user_id)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':

        # Get the login form data
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        if username == "admin" and password == "pdf2csv":
            print('hello me')

            user = User(user_id=1)

            # Log in the user
            login_user(user)

            return redirect(url_for('process'))

        else:
            flash(' Wrong Username/Password, please try again.', 'error')
            return redirect(url_for('index'))
    else:
        return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    # Log out the user
    logout_user()
    return redirect(url_for('index'))


@app.route('/process', methods=['GET','POST'])
@login_required
def process():
    return render_template('process.html')



@app.route('/upload', methods=['POST'])
@login_required
def upload():
    # Check if a file was uploaded
    if 'pdf_file' not in request.files:
        flash('No file uploaded.', 'error')
        return redirect(url_for('process'))

    file = request.files['pdf_file']


    # Check if the file has a valid extension
    if file.filename == '':
        return 'No file selected.'

    logger.error(f"hello world {file.filename}")

    if file and allowed_file(file.filename):
        filename = file.filename
        # mypath = "mysite/{}"

        # file_path = os.path.join(mypath.format(app.config['UPLOAD_FOLDER']), filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Create the 'uploads' directory if it does not exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)

        #try:
            # Extract text from the PDF file
        conversion_type = request.form.get('conversion_type')
        extracted_text = extract_pdf_data(file_path)


        save_to_mongo(extracted_text)
        # except:
        #     flash('Invalid file format! Please make sure to upload the correct PDF bill type.', 'error')
        #     return redirect(url_for('process'))


        flash('File uploaded and text extracted successfully.', 'success')
        return redirect(url_for('process'))
    else:
        flash('Invalid file format.', 'error')
        return redirect(url_for('process'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def extract_text_by_coordinates(pdf_path, page_num, rect):
    """
    Extracts text from a specified rectangular area on a PDF page.

    :param pdf_path: Path to the PDF file.
    :param page_num: Page number (starting from 0) to extract text from.
    :param rect: Tuple (left, top, right, bottom) representing the rectangular coordinates.
    :return: Extracted text from the specified area.
    """
    pdf_document = fitz.open(pdf_path)
    page = pdf_document[page_num]
    rect_region = fitz.Rect(*rect)
    text = page.get_text("text", clip=rect_region)
    pdf_document.close()
    return text


def is_arabic(text: str) -> bool:
    """
    Checks if the given text contains Arabic characters.

    Parameters
    ----------
    text : str
        The text to check.

    Returns
    -------
    bool
        True if the text contains Arabic characters, False otherwise.
    """
    for char in text:
        if '\u0600' <= char <= '\u06FF' or '\u0750' <= char <= '\u077F' or '\u08A0' <= char <= '\u08FF' or '\uFB50' <= char <= '\uFDFF' or '\uFE70' <= char <= '\uFEFF':
            return True
    return False


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def save_to_mongo(data):
    for _, extracted_text in data.items():
        collection.insert_one(extracted_text)

def fetch_all_documents():
    return list(collection.find({}, {'_id': 0}))

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
            flash('The Data Cleared Successfully.', 'success')
            # Delete all files in UPLOAD_FOLDER
            file_list = os.listdir(app.config['UPLOAD_FOLDER'])
            for file_name in file_list:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                os.remove(file_path)
        else:
            flash('There Is No Data To Clear.', 'info')
    except Exception as e:
        flash(f'Error clearing data: {str(e)}', 'error')
    return redirect(url_for('process'))


if __name__ == '__main__':
    app.run(debug=True)
