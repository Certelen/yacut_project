from settings import ALLOWED_CHAR, MAX_USER_SHORT

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_short(short_link):
    message = 'Указано недопустимое имя для короткой ссылки'
    if short_link is None:
        return False
    if URLMap.query.filter_by(short=short_link).first():
        raise InvalidAPIUsage(f'Имя "{short_link}" уже занято.')
    if len(short_link) > MAX_USER_SHORT:
        raise InvalidAPIUsage(message)
    for sym in short_link:
        if sym not in ALLOWED_CHAR:
            raise InvalidAPIUsage(message)
    return short_link


def validate_original(original_link):
    if URLMap.query.filter_by(original=original_link).first():
        exist_link = URLMap.query.filter_by(original=original_link).first()
        short_link = exist_link.short
        return short_link
    return False


def validate(original, short):
    if not original:
        raise InvalidAPIUsage('Вставьте длинную ссылку')
    if short:
        return validate_short(short)
    return validate_original(original)

def validate_data(data):
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
    return validate(link, user_short)