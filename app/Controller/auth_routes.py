from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from config import Config

import app.Model.user_models as user_models

from app.Controller.auth_forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required


from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER 
bp_auth.static_folder = Config.STATIC_FOLDER

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))       

    lform = LoginForm()
    if lform.validate_on_submit():

        user = user_models.User.query.filter_by(username = lform.username.data).first()

        if user is None or user.check_password(lform.password.data) == False:
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=lform.remember_me.data)
        return redirect(url_for('routes.index'))

    return render_template('login.html', title='Sign In', form=lform)


@bp_auth.route('/register', methods=['GET', 'POST']) 
def register():
    print('Enter REGISTER')
    if not current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    rform = RegisterForm()
    if rform.validate_on_submit():
        if rform.is_faculty.data:
            user = user_models.Faculty(username=rform.username.data,       email=rform.email.data,
                                    first_name=rform.first_name.data,   last_name=rform.last_name.data,
                                    wsu_id=rform.wsu_id.data,           phone_number=rform.phone_number.data
                                    )
        else:
            user = user_models.Student(username=rform.username.data,       email=rform.email.data,
                            first_name=rform.first_name.data,   last_name=rform.last_name.data,
                            wsu_id=rform.wsu_id.data,           phone_number=rform.phone_number.data
                            )
        user.set_password(rform.password1.data)
        user.save_to_db()
        flash(f'Welcome {user.first_name}! Account successfully created.')
        login_user(user, remember=False)
        return redirect(url_for('routes.index'))

    return render_template('register.html', form=rform)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
