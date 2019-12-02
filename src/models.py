from datetime import datetime, timedelta
from extensions import db


class URL(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    long_url = db.Column(db.String())
    short_url = db.Column(db.String(6), unique=True, default='')

    redirects = db.relationship('Redirect', back_populates='url')

    expiration = db.Column(db.DateTime, default=datetime.now() + timedelta(days=30))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<url {self.long_url}>"


class Redirect(db.Model):
    __tablename__ = 'redirect'
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.now())
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'))
    url = db.relationship("URL", backref='url')

    def __init__(self, url_id):
        self.url_id = url_id


class Error(db.Model):
    __tablename__ = 'error'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now())
    message = db.Column(db.String)

    def __init__(self, code, message):
        self.code = code
        self.message = message
