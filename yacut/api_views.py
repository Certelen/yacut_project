from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validate import validate
from .views import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def get_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage(
            'Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!')
    link = data['url']
    user_short = False
    if 'custom_id' in data:
        if not data['custom_id']:
            data['custom_id'] = None
        user_short = data['custom_id']
    val_check = validate(link, user_short, api=True)
    if val_check is True:
        short_link = get_unique_short_id()
        while URLMap.query.filter_by(short=short_link).first():
            short_link = get_unique_short_id()
    else:
        short_link = val_check
    url = URLMap(
        original=link,
        short=short_link
    )
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(
        {'short_link': url_for('redirect_url', url=short_link, _external=True), 'url': link}
    ), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_full_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': link.original}), HTTPStatus.OK
