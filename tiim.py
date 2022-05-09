import requests as rq
from bs4 import BeautifulSoup as bs4
import json


def tiim_login(lg, pwd):
    log_url = 'https://тиим.рф/personal/'
    results_url = 'https://тиим.рф/personal/'
    stages_url = 'https://тиим.рф'

    logload = {
        'login': lg,
        'password': pwd
    }
    s = rq.Session()

    log_ans = s.post(log_url, data=logload)
    check = True
    ans = {'ТИИМ': {'Ссылка': 'https://тиим.рф'}}
    ans1 = []
    ans2 = []

    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }

    res_html = s.get(results_url)
    res_bs = bs4(res_html.content, 'html.parser')

    r = res_bs.find_all('p')
    for a in r:
        if 'не принимали' in a.text or 'не допущены' in a.text:
            check = False

    dates_html = s.get(stages_url)
    dates_bs = bs4(dates_html.content, 'html.parser')

    r = dates_bs.find_all('p', id=True)

    for a in r:
        c = a.get_text(strip=True, separator='\n').splitlines()
        for temp in c:
            if 'Отборочный' in temp:
                sub = 'по математике' if not ans1 else 'по информатике'
                date = temp.replace('г.', '').replace('с', '').replace('по', '')
                date = date[date.index('—') + 1:].split()
                for word in range(len(date)):
                    if date[word] in months:
                        date[word] = months[date[word]]
                ans1.append((temp[:temp.index('—')] + sub, '.'.join(map(str, date[3:]))))

            elif 'Заключительный' in temp:  # and check:
                sub = 'по математике' if not ans2 else 'по информатике'
                date = temp.replace('г.', '')
                date = date[date.index('—') + 1:].split()
                for word in range(len(date)):
                    if date[word] in months:
                        date[word] = months[date[word]]
                ans2.append((temp[:temp.index('—')] + sub, '.'.join(map(str, date))))

    ans['ТИИМ']['Отборочные'] = ans1
    ans['ТИИМ']['Заключительные'] = ans2

    res = json.dumps(ans)

    return res
