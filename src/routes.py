from flask import Blueprint, render_template, request, redirect, jsonify, abort

from datetime import datetime, timedelta

import db_manager
from models import URL, Redirect, Error


short = Blueprint('short', __name__)


@short.route('/')
def index():
    return render_template('index.html')


@short.route('/add_url', methods=['POST'])
def add_url():
    long_url = request.json['url']
    url = db_manager.add_new_url(long_url)
    return jsonify(short_url=url.short_url)


@short.route('/<short_url>')
def redirect_to_url(short_url):
    try:
        url = URL.query.filter_by(short_url=short_url).first_or_404()
    except:
        abort(404)

    db_manager.log_redirect(url.id)

    return redirect(url.long_url)


@short.route('/stats')
def stats():
    # all url created
    total_urls = URL.query.count()

    last_minute_delta = datetime.now() - timedelta(minutes=1)
    last_hour_delta = datetime.now() - timedelta(hours=1)
    last_day_delta = datetime.now() - timedelta(days=1)

    # riderects
    total_redirects = Redirect.query.count()
    last_minute_redirects = Redirect.query.filter(Redirect.date_created > last_minute_delta).count()
    last_hour_redirects = Redirect.query.filter(Redirect.date_created > last_hour_delta).count()
    last_day_redirects = Redirect.query.filter(Redirect.date_created > last_day_delta).count()

    # errors
    total_errors = Error.query.count()
    last_minute_errors = Error.query.filter_by(code=400).filter(Error.time > last_minute_delta).count()
    last_hour_errors = Error.query.filter_by(code=400).filter(Error.time > last_hour_delta).count()
    last_day_errors = Error.query.filter_by(code=400).filter(Error.time > last_day_delta).count()

    return jsonify(
        total_urls=total_urls,
        total_redirects=total_redirects,
        last_minute_redirects=last_minute_redirects,
        last_hour_redirects=last_hour_redirects,
        last_day_redirects=last_day_redirects,
        total_errors=total_errors,
        last_minute_errors=last_minute_errors,
        last_hour_errors=last_hour_errors,
        last_day_errors=last_day_errors,
    )


@short.errorhandler(400)
def bad_request(e):
    db_manager.log_error(code=400, message=e.description)
    return "Bad Request"


@short.errorhandler(404)
def page_not_found(e):
    db_manager.log_error(code=404, message=e.description)
    return "PageNotFound"

