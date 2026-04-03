from flask import Blueprint , request , jsonify
import os
import csv
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime


upload = Blueprint('upload' , __name__)

UPLOAD_FOLDER = 'uploads'

@upload.route('/upload-csv' , methods=['POST'])
def upload_csv():
    
    if 'file' not in request.files:
        return jsonify({'error' : 'No file provided'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error' : 'Empty file name'}) ,400
    
    original_filename = secure_filename(file.filename)

    unique_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    file_name = f"{timestamp}_{unique_id}_{original_filename}"

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER),
    
    filepath = os.path.join(UPLOAD_FOLDER , file_name)


    file.save(filepath)

    headers = []
    with open (filepath , 'r' , newline='' , encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        total_rows = sum(1 for _ in reader)
   
    return jsonify({
        'message':'File uploaded successfully' ,
        'file_name' : file_name,
        'headers' : headers,
        'total_rows' : total_rows
    })
