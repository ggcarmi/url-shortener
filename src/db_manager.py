from urllib.parse import urlparse

import encoding_manager
from models import URL, Error, Redirect
from extensions import db


def log_error(code, message):
    error = Error(code=code, message=message)
    db.session.add(error)
    db.session.commit()


def log_redirect(id):
    redirect_obj = Redirect(id)
    db.session.add(redirect_obj)
    db.session.commit()


def add_new_url(long_url):
    if urlparse(long_url).scheme == '':
        long_url = 'http://' + long_url

    url = URL(long_url=long_url)
    db.session.add(url)
    db.session.flush()

    code = encoding_manager.generate_short_url()
    exist_hash = URL.query.filter_by(short_url=code).first()
    while exist_hash is not None:
        code = encoding_manager.generate_short_url()

    url.short_url = code
    db.session.commit()

    return url


