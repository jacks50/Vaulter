from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route('/')
    def home():
        return render_template('home.html')

    from .vaulture import vaulture_bp
    app.register_blueprint(vaulture_bp)

    return app
