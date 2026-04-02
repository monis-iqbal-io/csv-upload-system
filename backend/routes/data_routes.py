from flask import Blueprint, Flask, request, jsonify
from flask_cors import CORS
from utils.db import get_connection

app = Flask(__name__)
CORS(app)

data_bp = Blueprint('data', __name__)

@data_bp.route('/data', methods=['GET'])
def get_data():

    conn = get_connection()
    cursor = conn.cursor()

    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    file_name = request.args.get('file_name')

    base_query = "FROM users WHERE 1=1"
    params = []

    #ONLY apply if provided
    if file_name:
        base_query += " AND file_name = %s"
        params.append(file_name)

    if from_date and to_date:
        base_query += " AND date BETWEEN %s AND %s"
        params.extend([from_date, to_date])

    # DATA QUERY
    data_query = f"""
        SELECT name, mobile, email, city, date
        {base_query}
        ORDER BY id DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(data_query, params + [limit, offset])
    rows = cursor.fetchall()

    # convert tuple -> dict
    data = []
    for row in rows:
        data.append({
            "name": row[0],
            "mobile": row[1],
            "email": row[2],
            "city": row[3],
            "date": str(row[4]) if row[4] else None
        })

    # COUNT
    count_query = f"SELECT COUNT(*) {base_query}"
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": (total // limit) + (1 if total % limit else 0),
        "data": data
    })


@data_bp.route('/upload-history', methods=['GET'])
def upload_history():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        offset = (page - 1) * limit

        #MAIN QUERY
        cursor.execute("""
            SELECT file_name, total_rows, inserted_rows, updated_rows, status, upload_date
            FROM upload_files
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cursor.fetchall()

        data = []
        for row in rows:
            data.append({
                "file_name": row[0],
                "total_rows": row[1],
                "inserted": row[2],
                "updated": row[3],
                "status": row[4],
                "upload_date": row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else None
            })

        # COUNT QUERY
        cursor.execute("SELECT COUNT(*) FROM upload_files")
        total = cursor.fetchone()[0]

        conn.close()

        return jsonify({
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total // limit) + (1 if total % limit else 0),
            "data": data
        })

    except Exception as e:
        print(" ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

