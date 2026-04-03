from flask import Blueprint, request, jsonify
import os , json

mapping = Blueprint('mapping', __name__)

file_mappings = {}

ALLOWED_FIELDS = ["name", "mobile", "email", "city", "date"]

@mapping.route('/map-headers', methods=['POST'])
def map_headers():

    data = request.get_json()

    file_name = data.get('file_name')
    header_mapping = data.get('mapping')

    if not file_name:
        return jsonify({'error': 'file_name is required'}), 400

    if not header_mapping:
        return jsonify({'error': 'mapping is required'}), 400

    #CHECK ALL VALUES ARE VALID
    for field in header_mapping.values():
        if field not in ALLOWED_FIELDS:
            return jsonify({'error': f'Invalid field mapping: {field}'}), 400
    
    
    if 'mobile' not in header_mapping.values():
        return jsonify({'error': 'Mobile field mapping is required'}), 400
    
    
    for csv_header, mapped_field in header_mapping.items():

        if mapped_field == "mobile":

            header_lower = csv_header.lower()

        # Allow only mobile-like headers
            if not any(keyword in header_lower for keyword in ["mobile", "phone", "contact"]):
                return jsonify({
                    'error': f"Invalid mapping: '{csv_header}' cannot be mapped to 'mobile'"
            }), 400

    # CHECK DUPLICATES
    values = list(header_mapping.values())
    if len(values) != len(set(values)):
        return jsonify({'error': 'Duplicate mapping not allowed'}), 400

    BASE_DIR = os.getcwd()
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    mapping_path = os.path.join(UPLOAD_FOLDER, f"{file_name}_mapping.json")

    with open(mapping_path, 'w') as f:
        json.dump(header_mapping, f)

    return jsonify({
        'message': 'Mapping saved successfully',
        'file_name': file_name,
        'mapping': header_mapping
    })
    
    