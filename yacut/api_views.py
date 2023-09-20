from flask import jsonify, request, url_for
from settings import ALLOWED_CHAR

from . import app, db
from .models import URLMap
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage
from .validate import validate


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
    elif not val_check[0]:
        raise InvalidAPIUsage(val_check[1])
    else:
        short_link = val_check
    url = URLMap(
        original=link,
        short=short_link
    )
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify({'short_link': url_for('redirect_url', url=short_link, _external=True), 'url': link}), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_full_url(short_id):
    link = URLMap.query.filter_by(short=short_id).first()
    if link is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': link.original}), 200
