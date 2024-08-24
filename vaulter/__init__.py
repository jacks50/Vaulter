import os

from flask import Flask, render_template
from flask_cors import CORS


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(f'config.{os.getenv("VAULTER_APP", "Development")}Config')
    
    from .vaulter import vaulture_bp
    app.register_blueprint(vaulture_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app