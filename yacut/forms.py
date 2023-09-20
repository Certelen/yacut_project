from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import Length, Optional


class YacutForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка'
    )
    custom_id = URLField(
        'Пользовательский вариант короткой ссылки',
        validators=[Length(1, 16), Optional()]
    )
    create = SubmitField('Создать')
