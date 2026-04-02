from flask import Blueprint , request , jsonify
from routes.mapping_routes import file_mappings
from services.process_service import process_csv
import threading

process = Blueprint('process' , __name__)

@process.route('/start-upload' , methods = ['POST'])
def start_upload():
    data = request.get_json()

    file_name = data.get('file_name')

    if not file_name:
        return jsonify ({'error': 'file_name is required'}) , 400
    
    mapping = file_mappings.get(file_name)

    if not mapping:
        return jsonify({'error': 'Mapping not found for this file'}) , 400
    

    thread = threading.Thread(target=process_csv, args=(file_name, mapping))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message' : 'Processing Started' ,
        'file_name' : file_name
    })

