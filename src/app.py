from flask import Flask

from routes import short
from extensions import db


def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    db.init_app(app)
    app.register_blueprint(short)

    with app.app_context():

        db.create_all()
        return app


if __name__ == '__main__':
    app = create_app()
    app.run()


