import datetime
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    olymp = StringField('Название олимпиады', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Сохранить данные')


def unpack(olymp_list):
    olymps = []
    n = 1
    for olymp in olymp_list['olymps']:
        olymp_name = olymp
        quals, finals = [], []
        if 'Отборочные' in olymp_list['olymps'][olymp]:
            for qual in olymp_list['olymps'][olymp]['Отборочные']:
                print(qual)
                quals.append({
                    "id": n,
                    "name": olymp_name,
                    "stage": "Отборочный этап",
                    "date": qual[0],
                    "desc": qual[1],
                    "place": "Онлайн",
                    "reg": False,
                    "link": olymp_list['olymps'][olymp]['Ссылка']})
                n += 1
        if 'Заключительные' in olymp_list['olymps'][olymp]:
            for final in olymp_list['olymps'][olymp]["Заключительные"]:
                finals.append({
                    "id": n,
                    "name": olymp_name,
                    "stage": "Заключительный этап",
                    "date": final[0],
                    "desc": final[1],
                    "place": final[2],
                    "reg": False,
                    "link": olymp_list['olymps'][olymp]['Ссылка']})
                n += 1
        olymps.extend(quals)
        olymps.extend(finals)

    for a in range(len(olymps) - 1):
        print(olymps)
        for el in range(len(olymps) - a - 1):
            d1, m1, y1 = map(int, olymps[el]["date"].split('.'))
            d2, m2, y2 = map(int, olymps[el + 1]["date"].split('.'))
            date_1 = datetime.date(year=y1, month=m1, day=d1)
            date_2 = datetime.date(year=y2, month=m2, day=d2)
            if date_1 > date_2:
                olymps[el], olymps[el + 1] = olymps[el + 1], olymps[el]
    return olymps


def pu(olymps):
    olymps_passed = []
    olymps_upcoming = []
    for b in olymps:
        d, m, y = map(int, b["date"].split('.'))
        date = datetime.date(year=y, month=m, day=d)
        if date < datetime.date.today():
            olymps_passed.append(b)
        else:
            olymps_upcoming.append(b)
    return olymps_passed, olymps_upcoming

