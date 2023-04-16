from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, abort, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SubmitField, PasswordField
from wtforms.validators import Email, DataRequired
from . import db
from flask_bootstrap import Bootstrap
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

ad = Blueprint('ad', __name__)

class AdminForm(FlaskForm):
    def account_check(self, field):
        if field.data != 'mayData0426@gmail.com':
            raise ValidationError('Wrong Administrator')

    def password_check(self, field):
        if field.data != 'mayISOM4007':
            raise ValidationError('Wrong Administrator')

    email = StringField("Admin Email", validators=[DataRequired(message=''),
                                                   Email(message=u'Not an Email'), account_check])
    password = PasswordField("Admin Password", validators=[DataRequired(message=''), password_check])
    login = SubmitField("Login")

class AdminAddForm(FlaskForm):
    def email_unique(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Existing Email")

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), email_unique])
    password = StringField('Password', validators=[DataRequired()])
    add = SubmitField('Add User')


@ad.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()
    if form.validate_on_submit():
        session['admin'] = True
        return redirect(url_for('ad.control'))
    return render_template('form.html', form=form)

@ad.route('/control', methods=['GET', 'POST'])
def control():
    if not session.get('admin'):
        abort(400)
    users = User.query.all()
    return render_template('control.html', users=users)

@ad.route('/add', methods=['GET', 'POST'])
def admin_add():
    if not session.get('admin'):
        abort(400)
    form = AdminAddForm()
    if form.validate_on_submit():
        # n = []
        # for i in range(10):
        #     n.append(str(random.randint(0, 9)))
        # active_code = ''.join(n)
        user = User(username=request.form.get('username'), email=request.form.get('email'),
                    password= generate_password_hash(request.form.get('password'), method='sha256'))
        db.session.add(user)
        db.session.commit()
        flash('Add user successfully')
        return redirect(url_for('ad.admin_add'))
    return render_template('adminadd.html', form=form)

@ad.route('/delete', methods=['GET', 'POST'])
def admin_delete():
    if session.get('admin'):
        user = User.query.filter_by(id=request.form.get('id')).first()
        if user:
            db.session.delete(user)
            db.session.commit()
        return 'ok'
    abort(400)

@ad.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code='404'), 404

@ad.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code='500'), 500

@ad.errorhandler(400)
def bad_request(e):
    return render_template('error.html', code = '400'), 400
