from flask import Flask, render_template
import json
import datetime

app = Flask(__name__)


def unpack(olymp_list):
    olymps = []
    for olymp in olymp_list:
        olymp_name = olymp
        quals, finals = [], []
        for qual in olymp_list[olymp]["Отборочные"]:
            quals.append({
                "name": olymp_name,
                "stage": "Отборочный этап",
                "date": qual[0],
                "desc": qual[1],
                "place": "Онлайн",
                "link": qual[2]})
        for final in olymp_list[olymp]["Заключительные"]:
            finals.append({
                "name": olymp_name,
                "stage": "Заключительный этап",
                "date": final[0],
                "desc": final[1],
                "place": final[2],
                "link": final[3]})
        olymps.extend(quals)
        olymps.extend(finals)

    for a in range(len(olymps) - 1):
        for el in range(len(olymps) - a - 1):
            d1, m1, y1 = map(int, olymps[el]["date"].split('.'))
            d2, m2, y2 = map(int, olymps[el + 1]["date"].split('.'))
            date_1 = datetime.date(year=y1, month=m1, day=d1)
            date_2 = datetime.date(year=y2, month=m2, day=d2)
            if date_1 > date_2:
                olymps[el], olymps[el + 1] = olymps[el + 1], olymps[el]
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


@app.route('/', methods=['POST', 'GET'])
def based():
    with open("example.json", "rt", encoding="utf8") as Jason_Brody:
        f = Jason_Brody.read()
        olymp_list = json.loads(f)
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
    d = datetime.date.today()
    date = str(d.day) + " " + months[d.month - 1] + " " + str(d.year)
    olymps_passed, olymps_upcoming = unpack(olymp_list)
    return render_template('base.html', title="сайт", olymps_passed=olymps_passed, olymps_upcoming=olymps_upcoming, current_date=date)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)