from django.contrib.auth.decorators import login_required
from flask import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.functions import current_user

from forms import LoginForm, RegistrationForm, SettingsForm
from .db.orm import db_sessions

from db.orm.parts import Profile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ANIMAL_SITE'

db_sessions.global_init('db/database.sqlite')
login_manager = LoginManager(app)
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    session = db_sessions.create_session()
    user = session.query(Profile).filter(Profile.id == user_id).first()
    session.close()
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    global message
    logout_user()
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        session = db_sessions.create_session()
        user = session.query(Profile).filter(Profile.login == login).first()
        if not user:
            message = 'Данного пользователя нет. Пожалуйста, пройдите регистрацию.'
        elif not user.check_password(form.password.data):
            message = 'Введён неверный пароль'
        else:
            login_user(user, remember=form.remember_me.data)
            resp = redirect('/private')
            session.close()
            return resp
    resp = render_template('login.html', title='Ввойдите в свою учётную запись', form=form, message=message)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def create_account():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Profile(form.login.data,
                    form.password.data,
                    form.pet_name.data,
                    form.type.data,
                    form.age.data,
                    form.poroda.data)
        session = db_sessions.create_session()
        try:
            session.add(user)
            session.commit()
        except IntegrityError:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже существует.')
        except Exception as e:
            print(e)
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Произошла ошибка. Пожалуйста, повторите попытку позже.')
        finally:
            session.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def my_profile(user_login, user_pet_name, user_age, user_type, user_poroda):
    session = db_sessions.create_session()
    login = session.query(Profile).filter(Profile.login == user_login).first()
    pet_name = session.query(Profile).filter(Profile.pet_name == user_pet_name).first()
    age = session.query(Profile).filter(Profile.age == user_age).first()
    type = session.query(Profile).filter(Profile.type == user_type).first()
    poroda = session.query(Profile).filter(Profile.poroda == user_poroda).first()
    resp = render_template('account.html', title='Мой аккаунт', login=login, pet_name=pet_name,
                           age=age, type=type, poroda=poroda)
    session.close()
    return resp


@app.route('/cats', methods=['GET', 'POST'])
def cats_page():
    resp = render_template('cats.html', title='Породы кошек')
    return resp


@app.route('/cats', methods=['GET', 'POST'])
def dogs_page():
    resp = render_template('dogs.html', title='Породы собак')
    return resp


@app.route('/cats', methods=['GET', 'POST'])
def birds_page():
    resp = render_template('birds.html', title='Породы птиц')
    return resp


@app.route('/account/settings', methods=['GET', 'POST'])
@login_required
def settings_page():
    form = SettingsForm()
    session = db_sessions.create_session()
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    if form.validate_on_submit():
        if form.name.data:
            current_user.name = form.name.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        session.merge(current_user)
        session.commit()
        session.close()
        return redirect('/private')
    resp = render_template('settings.html', title='Настройки', form=form)
    session.close()
    return resp


if __name__ == '__main__':
    app.run()





