from flask import Flask
from flask_cors import CORS

from routes.main_routes import main
from routes.upload_routes import upload
from routes.mapping_routes import mapping
from routes.process_routes import process
from routes.data_routes import data_bp
from routes.status_routes import status_bp

app  = Flask(__name__)
CORS(app ,resources={r"/*": {"origins": "*"}})

app.register_blueprint(main)
app.register_blueprint(upload)
app.register_blueprint(mapping)
app.register_blueprint(process)
app.register_blueprint(data_bp)
app.register_blueprint(status_bp)

if __name__ == '__main__':
    app.run(debug=True)

