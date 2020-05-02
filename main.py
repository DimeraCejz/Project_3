from flask import Flask, render_template, redirect, abort, request
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from data.models import User, Pet, Feedback
from forms import LoginForm, RegistrationForm


from data import db_session
db_session.global_init("database/profile_info.sqlite")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'animal_site'
login_manager = LoginManager(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user


@app.route('/login', methods=['GET', 'POST'])
def sign_in_page():
    logout_user()
    message = ''
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        session = db_session.create_session()
        user = session.query(User).filter(User.login == login).first()
        if not user:
            message = 'Данного пользователя нет. Пожалуйста, пройдите регистрацию.'
        elif not user.check_password(form.password.data):
            message = 'Введён неверный пароль'
        else:
            login_user(user, remember=form.remember_me.data)
            resp = redirect('/main')
            session.close()
            return resp
    resp = render_template('login.html', title='Авторизация', form=form, message=message)
    return resp


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.login.data,
                    form.password.data)
        session = db_session.create_session()
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            return render_template('registration.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже существует.')
        except Exception as e:
            print(e)
            return render_template('registration.html', title='Регистрация', form=form,
                                   message='Произошла ошибка. Пожалуйста, повторите попытку позже.')
        finally:
            session.close()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/')
@app.route('/main')
@login_required
def main_page():
    session = db_session.create_session()
    session.add(current_user)
    session.merge(current_user)
    resp = render_template('main_page.html', title='Основная страница')
    session.close()
    return resp


if __name__ == '__main__':
    app.run()