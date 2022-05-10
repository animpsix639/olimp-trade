import json
import requests as rq
from bs4 import BeautifulSoup as bs4
import re
import pymorphy2


def granit_login(lg, pwd):
    subjects = ['Химия', 'Естественные науки', 'Экология', 'Информатика']
    final_subjects = []

    morph = pymorphy2.MorphAnalyzer()

    dates_url = 'https://ogn.spmi.ru'
    log_url = 'http://olimpiada.spmi.ru/login/index.php'
    stages_url = 'http://olimpiada.spmi.ru/course/view.php?id=4'

    ans = {'Гранит науки': {'Ссылка': 'https://ogn.spmi.ru'}}

    logload = {
        'username': lg,
        'password': pwd
    }

    s = rq.Session()
    log_ans = s.post(log_url, data=logload)

    res_html = s.get(stages_url)
    res_bs = bs4(res_html.content, 'html.parser')
    [final_subjects.append(subject) for subject in subjects if not re.search(subject, ' '.join(
        [x.find('strong').text for x in res_bs.find_all('div', class_='availabilityinfo')]))]

    dates_html = s.get(dates_url)
    dates_bs = bs4(dates_html.content, 'html.parser')

    a = dates_bs.find_all('p')
    for r in a:
        t = r.time
        if t:
            c = r.strong.text
            if 'Старт' in c:
                ans['Гранит науки']['Отборочные'] = (t.text, c)
            elif 'Заключительный' in c and any([True if (morph.parse(x)[0].inflect({'datv'}).word in c) or (
                    'Естественным' in c and 'Естественные науки' in final_subjects) else False for x in
                                                final_subjects]):
                ans['Гранит науки']['Заключительные'] = (t.text, c)

    ret = json.dumps(ans)

    return ret

