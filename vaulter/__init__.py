import os

from flask import Flask, render_template
from .vaulter import vaulture_bp
from .file_manager import get_file_manager

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f'config.{os.getenv("VAULTER_APP", "Development")}Config')

    with app.app_context():
        file_mgr = get_file_manager()

    print(file_mgr)

    @app.route('/')
    def home():
        return render_template('home.html')

    app.register_blueprint(vaulture_bp)

    return app