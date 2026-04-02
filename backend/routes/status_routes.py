from flask import Blueprint, request, jsonify
from services.process_service import progress_store

status_bp = Blueprint('status_bp', __name__)

@status_bp.route('/upload-status', methods=['GET'])
def upload_status():

    file_name = request.args.get('file_name')

    if not file_name:
        return jsonify({'error': 'file_name is required'}), 400

    #RETURN LIVE DATA
    if file_name in progress_store:
        return jsonify(progress_store[file_name])

    return jsonify({
        "status": "processing",
        "progress": 0,
        "inserted": 0,
        "updated": 0,
        "total": 0
    })