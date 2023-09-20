from settings import ALLOWED_CHAR
from .models import URLMap


def validate_short(short_link, api=False):
    if short_link is None:
        return True
    if URLMap.query.filter_by(short=short_link).first():
        if api:
            return False, f'Имя "{short_link}" уже занято.'
        return False, f'Имя {short_link} уже занято!'
    if len(short_link) > 16:
        return False, 'Указано недопустимое имя для короткой ссылки'
    for sym in short_link:
        if sym not in ALLOWED_CHAR:
            return False, 'Указано недопустимое имя для короткой ссылки'
    return short_link


def validate_original(original_link):
    if URLMap.query.filter_by(original=original_link).first():
        exist_link = URLMap.query.filter_by(original=original_link).first()
        short_link = exist_link.short
        return short_link
    return True


def validate(original, short, api=False):
    if not original:
        return False, 'Вставьте длинную ссылку'
    if short:
        return validate_short(short, api)
    return validate_original(original)
