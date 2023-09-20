from random import choice
from flask import flash, render_template, abort, redirect
from settings import ALLOWED_CHAR

from . import app, db
from .forms import YacutForm
from .models import URLMap
from .validate import validate


def get_unique_short_id():
    short_link = ""
    for _ in range(6):
        short_link += choice(ALLOWED_CHAR)
    return short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = YacutForm()
    if form.validate_on_submit():
        user_short = form.custom_id.data
        link = form.original_link.data
        val_check = validate(link, user_short)
        if val_check is True:
            short_link = get_unique_short_id()
            while URLMap.query.filter_by(short=short_link).first():
                short_link = get_unique_short_id()
        elif not val_check[0]:
            flash(val_check[1], 'free-message')
            return render_template('index.html', form=form)
        else:
            short_link = val_check
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
    link = URLMap.query.filter_by(short=url).first()
    if link is None:
        abort(404)
    return redirect(link.original)
