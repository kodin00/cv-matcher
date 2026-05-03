from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Blueprints registered as each epic is completed
from routes.health import health_bp
from routes.jobs   import jobs_bp
from routes.match  import match_bp

app.register_blueprint(health_bp, url_prefix="/api")
app.register_blueprint(jobs_bp,   url_prefix="/api")
app.register_blueprint(match_bp,  url_prefix="/api")

# Pre-load model at startup to avoid cold start on first request
from services.embedding_service import get_model
get_model()

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False, port=5000)
