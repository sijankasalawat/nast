

# from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, url_for
# import os
# from pymongo import MongoClient
# from bson import ObjectId  # Import to handle ObjectId serialization
# from combine import process_certificate, validate_marksheet_against_certificate, process_marksheet
# from autofill import read_csv_data, save_to_pdf, save_to_database

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['CERTIFICATES_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates')
# app.config['MARKSHEETS_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'marksheets')
# app.config['PROCESSED_FOLDER'] = 'processed'
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
# app.secret_key = 'supersecretkey'  # Required for flashing messages

# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])
# if not os.path.exists(app.config['CERTIFICATES_FOLDER']):
#     os.makedirs(app.config['CERTIFICATES_FOLDER'])
# if not os.path.exists(app.config['MARKSHEETS_FOLDER']):
#     os.makedirs(app.config['MARKSHEETS_FOLDER'])
# if not os.path.exists(app.config['PROCESSED_FOLDER']):
#     os.makedirs(app.config['PROCESSED_FOLDER'])

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# # Helper function to serialize ObjectId
# def serialize_data(data):
#     if isinstance(data, list):
#         return [serialize_data(item) for item in data]
#     if isinstance(data, dict):
#         return {key: serialize_data(value) for key, value in data.items()}
#     if isinstance(data, ObjectId):
#         return str(data)
#     return data

# @app.route('/')
# def home():
#     return render_template('home.html')


# @app.route('/index', methods=['GET', 'POST'])
# def upload_files():
#     if request.method == 'POST':
#         if 'certificate' not in request.files or 'marksheet' not in request.files:
#             return jsonify({'success': False, 'message': 'No file part'}), 400

#         certificate = request.files['certificate']
#         marksheet = request.files['marksheet']

#         if certificate.filename == '' or marksheet.filename == '':
#             return jsonify({'success': False, 'message': 'No selected file'}), 400

#         if allowed_file(certificate.filename) and allowed_file(marksheet.filename):
#             certificate_path = os.path.join(app.config['CERTIFICATES_FOLDER'], certificate.filename)
#             marksheet_path = os.path.join(app.config['MARKSHEETS_FOLDER'], marksheet.filename)

#             certificate.save(certificate_path)
#             marksheet.save(marksheet_path)

#             # Process files
#             csv_path = os.path.join(app.config['PROCESSED_FOLDER'], 'combined_results.csv')
#             certificate_output_folder = os.path.join(app.config['PROCESSED_FOLDER'], 'certificate_result')
#             marksheet_output_folder = os.path.join(app.config['PROCESSED_FOLDER'], 'mark_images')

#             certificate_data = process_certificate(certificate_path, certificate_output_folder, csv_path)

#             if validate_marksheet_against_certificate(marksheet_path, certificate_data):
#                 process_marksheet(marksheet_path, marksheet_output_folder, csv_path, certificate_data)
                
#                 data = read_csv_data(csv_path)
#                 if data:
#                     student_data = data[0] 
#                 return jsonify({'success': True, 'student_data': serialize_data(student_data)}), 200
#             else:
#                 return jsonify({'success': False, 'message': 'Marksheet validation failed: The marksheet does not belong to the certificate holder.'}), 400

#         return jsonify({'success': False, 'message': 'File type not allowed'}), 400

#     return render_template('index.html')

# @app.route('/save', methods=['POST'])
# def save_form():
#     student_data = request.form.to_dict()
#     save_to_database(student_data)
#     serialized_data = serialize_data(student_data)
#     return jsonify({'success': True, 'message': 'Data saved successfully!', 'student_data': serialized_data}), 200

# @app.route('/download', methods=['GET'])
# def download_pdf():
#     symbol_no = request.args.get('Symbol_No')

#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["college_registration"]
#     collection = db["students"]
#     existing_student = collection.find_one({"Symbol_No": symbol_no})

#     if existing_student:
#         pdf_path = save_to_pdf(existing_student)
#         return jsonify({'success': True, 'pdf_url': url_for('processed', filename=pdf_path.split('/')[-1])}), 200
#     else:
#         return jsonify({'success': False, 'message': 'Data must be saved before downloading the PDF.'}), 400

# @app.route('/generate-pdf', methods=['POST'])
# def handle_generate_pdf():
#     data = request.get_json()
#     pdf_path = save_to_pdf(data)
#     return jsonify({'pdf_url': f'/downloads/{os.path.basename(pdf_path)}'})

# @app.route('/downloads/<filename>')
# def download_file(filename):
#     return send_from_directory('processed', filename, as_attachment=True)

# @app.route('/download', methods=['GET'])
# def download_pdf():
#     symbol_no = request.args.get('Symbol_No')

#     # Ensure the symbol number is correct
#     print(f"Symbol Number: {symbol_no}")  

#     client = MongoClient("mongodb://localhost:27017/")
#     db = client["college_registration"]
#     collection = db["students"]
#     existing_student = collection.find_one({"Symbol_No": symbol_no})

#     # Verify that the correct student data is retrieved
#     if existing_student:
#         print(f"Existing Student Data: {existing_student}")  # Debugging output

#         pdf_path = save_to_pdf(existing_student)
#         print(f"Generated PDF Path: {pdf_path}")  # Debugging output

#         if pdf_path:
#             return jsonify({'success': True, 'pdf_url': url_for('processed', filename=pdf_path.split('/')[-1])}), 200
#         else:
#             print("PDF generation failed.")  # Debugging output
#             return jsonify({'success': False, 'message': 'PDF generation failed.'}), 500
#     else:
#         print("No matching student found.")  # Debugging output
#         return jsonify({'success': False, 'message': 'Data must be saved before downloading the PDF.'}), 400

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory, url_for
import os
import json

from pymongo import MongoClient
from bson import ObjectId  # Import to handle ObjectId serialization
from combine import process_certificate, validate_marksheet_against_certificate, process_marksheet
from autofill import read_csv_data, save_to_pdf, save_to_database
from combine import process_certificate, validate_marksheet_against_certificate, process_marksheet

from watermark import detect_watermark_frequency  # Correct function name
 # Import the watermark detection function

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CERTIFICATES_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'certificates')
app.config['MARKSHEETS_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'marksheets')
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'supersecretkey'  # Required for flashing messages

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['CERTIFICATES_FOLDER']):
    os.makedirs(app.config['CERTIFICATES_FOLDER'])
if not os.path.exists(app.config['MARKSHEETS_FOLDER']):
    os.makedirs(app.config['MARKSHEETS_FOLDER'])
if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Helper function to serialize ObjectId
def serialize_data(data):
    if isinstance(data, list):
        return [serialize_data(item) for item in data]
    if isinstance(data, dict):
        return {key: serialize_data(value) for key, value in data.items()}
    if isinstance(data, ObjectId):
        return str(data)
    return data

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'certificate' not in request.files or 'marksheet' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'}), 400

        certificate = request.files['certificate']
        marksheet = request.files['marksheet']

        if certificate.filename == '' or marksheet.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'}), 400

        if allowed_file(certificate.filename) and allowed_file(marksheet.filename):
            certificate_path = os.path.join(app.config['CERTIFICATES_FOLDER'], certificate.filename)
            marksheet_path = os.path.join(app.config['MARKSHEETS_FOLDER'], marksheet.filename)

            certificate.save(certificate_path)
            marksheet.save(marksheet_path)

            # Detect watermarks
            if not detect_watermark_frequency(certificate_path) or not detect_watermark_frequency(marksheet_path):
                return jsonify({'success': False, 'message': 'One or both files do not contain the required watermark.'}), 400

            # Process files
            csv_path = os.path.join(app.config['PROCESSED_FOLDER'], 'combined_results.csv')
            certificate_output_folder = os.path.join(app.config['PROCESSED_FOLDER'], 'certificate_result')
            marksheet_output_folder = os.path.join(app.config['PROCESSED_FOLDER'], 'mark_images')

            certificate_data = process_certificate(certificate_path, certificate_output_folder, csv_path)

            if certificate_data is None:
                return jsonify({'success': False, 'message': 'Error processing certificate. No data extracted.'}), 400

            if validate_marksheet_against_certificate(marksheet_path, certificate_data):
                process_marksheet(marksheet_path, marksheet_output_folder, csv_path, certificate_data)
                
                data = read_csv_data(csv_path)
                if data:
                    student_data = data[0]  # Assuming one student's data per file
                    return jsonify({'success': True, 'student_data': serialize_data(student_data)}), 200
                else:
                    return jsonify({'success': False, 'message': 'Failed to read processed data.'}), 400
            else:
                return jsonify({'success': False, 'message': 'Marksheet validation failed: The marksheet does not belong to the certificate holder.'}), 400

        return jsonify({'success': False, 'message': 'File type not allowed'}), 400

    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_form():
    student_data = request.form.to_dict()
    symbol_no = student_data.get('Symbol_No')

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["college_registration"]
    collection = db["students"]

    # Save or update the student's data
    existing_student = collection.find_one({"Symbol_No": symbol_no})
    if existing_student:
        collection.update_one({"Symbol_No": symbol_no}, {"$set": student_data})
    else:
        collection.insert_one(student_data)

    return jsonify({'success': True, 'message': 'Data saved successfully!', 'student_data': serialize_data(student_data)}), 200

@app.route('/generate-pdf', methods=['POST'])
def handle_generate_pdf():
    data = request.get_json()  # Parse the incoming JSON data correctly

    if isinstance(data, str):
        try:
            data = json.loads(data)  # Convert string to dictionary if necessary
        except json.JSONDecodeError:
            return jsonify({'success': False, 'message': 'Invalid JSON received.'}), 400

    if not data:
        return jsonify({'success': False, 'message': 'No data received or invalid JSON.'}), 400

    symbol_no = data.get('Symbol_No')

    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["college_registration"]
    collection = db["students"]

    # Check if the student's data exists
    existing_student = collection.find_one({"Symbol_No": symbol_no})
    if not existing_student:
        return jsonify({'success': False, 'message': 'Data must be saved before generating PDF.'}), 400

    # Generate the PDF
    pdf_path = save_to_pdf(existing_student)
    return jsonify({'pdf_url': f'/downloads/{os.path.basename(pdf_path)}'})

@app.route('/downloads/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    print(f"Serving file from: {file_path}")  # Debugging log
    if not os.path.exists(file_path):
        return jsonify({'success': False, 'message': 'File not found.'}), 404
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
