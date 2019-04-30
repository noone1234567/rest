from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired


class AddSolutionForm(FlaskForm):
    task = StringField('Задача', validators=[DataRequired()])
    code = TextAreaField('Код', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    group = StringField('Группа', validators=[DataRequired()])
    year = SelectField("Год обучения", coerce=int, choices=[(1, "1"), (2, "2")])
    submit = SubmitField('Зарегистрироваться')


class StatusPreviewForm(FlaskForm):
    status = SelectField("Статус", choices=[("На проверке", "На проверке"), ("Зачтено", "Зачтено"), ("На доработке",
                                                                                                     "На доработке")])
    submit = SubmitField('Изменить')


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
