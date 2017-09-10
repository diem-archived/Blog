from datetime import datetime

from flask import current_app, redirect, render_template, session, url_for

from . import main
from .. import db
from ..email import send_email
from ..models import User
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if current_app.config['Blog_ADMIN']:
                send_email(
                    current_app.config['BLOG_ADMIN'],
                    'New User',
                    'mail/new_user',
                    user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known', False),
        current_time=datetime.utcnow())
