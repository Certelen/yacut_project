from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional

from settings import MAX_USER_SHORT, MIN_USER_SHORT


class YacutForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка'
    )
    custom_id = URLField(
        'Пользовательский вариант короткой ссылки',
        validators=[Length(MIN_USER_SHORT, MAX_USER_SHORT), Optional()]
    )
    create = SubmitField('Создать')
