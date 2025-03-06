from flask import Flask, render_template, request, flash, redirect, url_for, send_file
import os
from core_utils import extract_pdf_data
import fitz
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import psycopg2
import logging
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'your_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig()
logger = logging.getLogger(__name__)

# Create a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='pdf2csv2-4399.postgres.pythonanywhere-services.com',
    port='14399',
    database='postgres',
    user='super',
    password='super@pdf2csv#',
    sslmode="disable"
)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_txt (
                    id serial PRIMARY KEY,
                    Customer varchar(200),
                    Customer_No varchar(200),
                    Account_No varchar(200),
                    Meter_No varchar(200),
                    Previous_Reading_Date varchar(200),
                    Previous_Reading varchar(200),
                    Current_Reading_Date varchar(200),
                    Current_Reading varchar(200),
                    Due_Date varchar(200),
                    Reading_Type varchar(200),
                    Tariff_Type varchar(200),
                    Invoice_Month varchar(200),
                    Government_Subsidy varchar(200),
                    Consumption_KWH_1 varchar(200),
                    Rate_1 varchar(200),
                    Consumption_KWH_2 varchar(200),
                    Rate_2 varchar(200),
                    Consumption_KWH_3 varchar(200),
                    Rate_3 varchar(200),
                    Consumption_KWH_4 varchar(200),
                    Rate_4 varchar(200),
                    Consumption_KWH_5 varchar(200),
                    Rate_5 varchar(200),
                    Consumption_KWH_6 varchar(200),
                    Rate_6 varchar(200),
                    Total_Before_VAT varchar(200),
                    VAT varchar(200),
                    Total_After_VAT varchar(200),
                    Total_Payable_Amount varchar(200)
                );
                ''')


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
    print('hello from process')
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


        extracted_text = extract_pdf_data(file_path)
        save_to_postgres(extracted_text)
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


def save_to_postgres(data):
    for page, extracted_text in data.items():
        cursor = conn.cursor()
        keys = extracted_text.keys()
        values = [extracted_text[key] for key in keys]
        insert_query = "INSERT INTO extracted_txt ({}) VALUES ({})".format(
            ', '.join(keys),
            ', '.join(['%s'] * len(keys))
        )
        cursor.execute(insert_query, tuple(values))
        conn.commit()
        cursor.close()

@app.route('/download_csv', methods=['GET'])
@login_required
def download_csv():
    # Retrieve the extracted text from PostgreSQL
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM extracted_txt")
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows)
        # mypath = "mysite/{}"
        # csv_path = os.path.join(mypath.format(app.config['UPLOAD_FOLDER']), 'Tasdeed.csv')
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Tasdeed.csv')

        # Capitalize the first row (header) in uppercase
        header = [desc[0] for desc in cursor.description]
        header = [(col.upper()).replace("_", " ") for col in header]
        df.columns = header

        # Save the DataFrame as a CSV file
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')

        return send_file('/home/pdf2csv2/uploads/Tasdeed.csv', mimetype='text/csv', as_attachment=True)

    flash('No extracted text found.', 'error')
    return redirect(url_for('process'))



@app.route('/clear_table', methods=['GET'])
@login_required
def clear_table():
    # Check if the table is empty
    # cursor = conn.cursor()
    # cursor.execute("SELECT COUNT(*) FROM extracted_txt")
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM extracted_txt")
            count = cursor.fetchone()[0]
            # if count > 0:
            #     cursor.execute("TRUNCATE TABLE extracted_txt")
            # conn.commit()
            # flash('Data cleared successfully.', 'success' if count > 0 else 'No data to clear.', 'info')


            if count > 0:
                # Drop the table from the database
                cursor.execute("DROP TABLE extracted_tXt")
                conn.commit()

                # Recreate the table with the same structure
                cursor.execute('''CREATE TABLE IF NOT EXISTS extracted_txt (
                                    id serial PRIMARY KEY,
                                    Customer varchar(200),
                                    Customer_No varchar(200),
                                    Account_No varchar(200),
                                    Meter_No varchar(200),
                                    Previous_Reading_Date varchar(200),
                                    Previous_Reading varchar(200),
                                    Current_Reading_Date varchar(200),
                                    Current_Reading varchar(200),
                                    Due_Date varchar(200),
                                    Reading_Type varchar(200),
                                    Tariff_Type varchar(200),
                                    Invoice_Month varchar(200),
                                    Government_Subsidy varchar(200),
                                    Consumption_KWH_1 varchar(200),
                                    Rate_1 varchar(200),
                                    Consumption_KWH_2 varchar(200),
                                    Rate_2 varchar(200),
                                    Consumption_KWH_3 varchar(200),
                                    Rate_3 varchar(200),
                                    Consumption_KWH_4 varchar(200),
                                    Rate_4 varchar(200),
                                    Consumption_KWH_5 varchar(200),
                                    Rate_5 varchar(200),
                                    Consumption_KWH_6 varchar(200),
                                    Rate_6 varchar(200),
                                    Total_Before_VAT varchar(200),
                                    VAT varchar(200),
                                    Total_After_VAT varchar(200),
                                    Total_Payable_Amount varchar(200)
                                );
                                ''')
                conn.commit()
                flash('The Data Cleared Successfully.', 'success')
                # Delete all files in UPLOAD_FOLDER
                # mypath = "mysite/{}"
                # file_list = os.listdir(mypath.format(app.config['UPLOAD_FOLDER']))
                file_list = os.listdir(app.config['UPLOAD_FOLDER'])
                for file_name in file_list:
                    # mypath = "mysite/{}"
                    # file_path = os.path.join(mypath.format(app.config['UPLOAD_FOLDER']), file_name)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                    os.remove(file_path)
            else:
                flash('There Is No Data To Clear.', 'info')

    except Exception as e:
        conn.rollback()  # Rollback the transaction on error
        flash('Error clearing data: {}'.format(str(e)), 'error')
    finally:
        return redirect(url_for('process'))


if __name__ == '__main__':
    app.run(debug=True)
