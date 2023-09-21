from random import choice

from flask import flash, redirect, render_template

from settings import ALLOWED_CHAR, SYM_RANDOM_SHORT

from . import app, db
from .error_handlers import InvalidAPIUsage
from .forms import YacutForm
from .models import URLMap
from .validate import validate


def get_unique_short_id():
    short_link = ""
    for _ in range(SYM_RANDOM_SHORT):
        short_link += choice(ALLOWED_CHAR)
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        user_short = form.custom_id.data
        link = form.original_link.data
        try:
            short_link = validate(link, user_short)
        except InvalidAPIUsage as error:
            message = error.message
            if 'занято' in message:
                message = f'Имя {user_short} уже занято!'
            flash(message, 'free-message')
            return render_template('index.html', form=form)
        if short_link is False:
            short_link = get_unique_short_id()
            while URLMap.query.filter_by(short=short_link).first():
                short_link = get_unique_short_id()
        urlmap = URLMap(
            original=link,
            short=short_link,
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template(
            'index.html',
            form=form,
            short_link=short_link
        )
    return render_template('index.html', form=form)


@app.route('/<string:url>')
def redirect_url(url):
    link = URLMap.query.filter_by(short=url).first_or_404()
    return redirect(link.original)
