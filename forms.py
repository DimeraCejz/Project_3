from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    login = StringField('Имя пользователя:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    pet_name = StringField('Имя питомца:', validators=[DataRequired()])
    age = IntegerField('Возраст питомца:', validators=[DataRequired()])
    type = StringField('Вид:', validators=[DataRequired()])
    poroda = StringField('Порода:', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class SettingsForm(FlaskForm):
    login = StringField('Имя:')
    email = StringField('Логин:')
    password = PasswordField('Пароль:')
    check_password = PasswordField('Повторите пароль:',
                                   validators=[EqualTo(fieldname='password', message='Пароли должны совпадать!')])
    pet_name = StringField('Имя питомца:')
    age = IntegerField('Возраст питомца:')
    type = StringField('Вид:')
    poroda = StringField('Порода:')
    submit = SubmitField('Изменить')


