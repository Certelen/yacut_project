from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validate import validate_data
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_short_url():
    data = request.get_json()
    val_check = validate_data(data)
    if val_check is False:
        short_link = get_unique_short_id()
        while URLMap.query.filter_by(short=short_link).first():
            short_link = get_unique_short_id()
    else:
        short_link = val_check
    url = URLMap(
        original=data['url'],
        short=short_link
    )
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {'short_link': url_for('redirect_url', url=short_link, _external=True), 'url': data['url']}
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_full_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
