from flask import Flask, render_template, request
import json
import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def based():
    with open("example.json", "rt", encoding="utf8") as Jason_Brody:
        f = Jason_Brody.read()
        olymp_list = json.loads(f)
    months = ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября", "Декабря"]
    d = datetime.date.today()
    date = str(d.day) + " " + months[d.month - 1] + " " + str(d.year)
    olymp_list_new = []
    c = 'любого'

    if request.method == 'POST':
        c = request.form["class"]
        for n in range(len(olymp_list["olymps"])):
            olymp = olymp_list["olymps"][n]
            classmin, classmax = map(int, olymp["classes"].split('-'))
            if classmin <= int(c) <= classmax:
                olymp_list_new.append(olymp)
    if c == 'любого':
        olymp_list_new = olymp_list
    else:
        olymp_list_new = {"olymps": olymp_list_new}
    return render_template('olymp_trade.html', title="сайт", olymps=olymp_list_new, current_date=date, clas=c)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)