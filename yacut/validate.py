from flask import flash

from settings import ALLOWED_CHAR, MAX_USER_SHORT

from .error_handlers import InvalidAPIUsage
from .models import URLMap


def validate_short(short_link, api=False):
    message = 'Указано недопустимое имя для короткой ссылки'
    if short_link is None:
        return True
    if URLMap.query.filter_by(short=short_link).first():
        if api:
            raise InvalidAPIUsage(f'Имя "{short_link}" уже занято.')
        return False, f'Имя {short_link} уже занято!'
    if len(short_link) > MAX_USER_SHORT:
        if api:
            raise InvalidAPIUsage(message)
        return False, message
    for sym in short_link:
        if sym not in ALLOWED_CHAR:
            if api:
                raise InvalidAPIUsage(message)
            return False, message
    return short_link


def validate_original(original_link):
    if URLMap.query.filter_by(original=original_link).first():
        exist_link = URLMap.query.filter_by(original=original_link).first()
        short_link = exist_link.short
        return short_link
    return True


def validate(original, short, api=False):
    if not original:
        if api:
            raise InvalidAPIUsage('Вставьте длинную ссылку')
        return False, 'Вставьте длинную ссылку'
    if short:
        return validate_short(short, api)
    return validate_original(original)
