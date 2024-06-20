from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    @app.route()
    def home():
        return '<p>HOME</p>'

    from . import vaulture
    app.register_blueprint(vaulture)

    return app
