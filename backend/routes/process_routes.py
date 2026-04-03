from flask import Blueprint , request , jsonify
from routes.mapping_routes import file_mappings
from services.process_service import process_csv
import threading
import os , json
process = Blueprint('process' , __name__)

@process.route('/start-upload' , methods = ['POST'])
def start_upload():
    data = request.get_json()

    file_name = data.get('file_name')

    if not file_name:
        return jsonify ({'error': 'file_name is required'}) , 400

    BASE_DIR = os.getcwd()
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    mapping_path = os.path.join(UPLOAD_FOLDER, f"{file_name}_mapping.json")

    if not os.path.exists(mapping_path):
        return jsonify({'error': 'Mapping not found for this file'}) , 400

    with open(mapping_path, 'r') as f:
        mapping = json.load(f)
    
    

    if not mapping:
        return jsonify({'error': 'Mapping not found for this file'}) , 400
    

    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    thread = threading.Thread(target=process_csv, args=(file_path, mapping))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message' : 'Processing Started' ,
        'file_name' : file_name
    })

