from flask import Flask, render_template, redirect, request
import json
import datetime
from funcs import unpack, pu, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bebra'

logins = []
user_login = False


@app.route('/',  methods=['POST', 'GET'])
@app.route('/home',  methods=['POST', 'GET'])
def based():
    if user_login:
        with open("example.json", "rt", encoding="utf8") as Jason_Brody:
            f = Jason_Brody.read()
            olymp_list = json.loads(f)
        olymps = unpack(olymp_list)
        olymps_passed, olymps_upcoming = pu(olymps)
    else:
        olymps_passed = olymps_upcoming = []
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
    d = datetime.date.today()
    date = str(d.day) + " " + months[d.month - 1] + " " + str(d.year)
    return render_template('base.html', title="сайт", olymps_passed=olymps_passed, olymps_upcoming=olymps_upcoming, current_date=date)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    dt = LoginForm().data
    if dt["submit"]:
        global user_login
        user_login = True
        logins.append(dt)
        with open("olymp_logins.json", "w", encoding="utf8") as file:
            json.dump(logins, file, ensure_ascii=False, indent=2)
    return render_template('login_field.html', title='Авторизация', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
