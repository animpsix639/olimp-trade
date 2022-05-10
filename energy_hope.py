import requests as rq
from bs4 import BeautifulSoup as bs4
import re

def energy_hope_login(lg, pwd):
    log_url = 'https://www.energy-hope.ru/cabinet/profile.html'
    results_url = 'https://www.energy-hope.ru/cabinet/results.html'
    stages_url = 'https://www.energy-hope.ru/cabinet/stages.html'

    logload = {
        'logon_status': 1,
        'logon_name': lg,
        'logon_pwd': pwd,
        'btnLogon.x': 64,
        'btnLogon.y': 21
    }
    s = rq.Session()

    t1 = []
    t2 = []

    ans = {'olymps': {'Надежда энергетики': {'Ссылка': 'https://www.energy-hope.ru'}}}
    ans1 = []
    ans2 = []

    log_ans = s.post(log_url, data=logload)

    res_html = s.get(log_ans.url)
    res_bs = bs4(res_html.content, 'html.parser')

    ac1 = res_bs.find_all('div', class_='title1')
    if not ac1:
        print('НЕВЕРНЫЙ ЛОГИН ИЛИ ПАРОЛЬ')

    res_html = s.get(results_url)
    res_bs = bs4(res_html.content, 'html.parser')

    ac2 = res_bs.find_all('div', class_="ui-state-default ui-corner-all")
    for cont in ac2:
        rs = cont.text
        check = rs.find('отборочного')
        subj = re.split('по предмету', rs)[1].split()[0][:-1]
        t1.append(subj) if check else t2.append(subj)

    tab_html = s.get(stages_url)
    tab_bs = bs4(tab_html.content, 'html.parser')

    tab2 = tab_bs.find_all('div', id='tabs-2')
    tab2_content = [v.find_all('h3') for v in tab2][0]
    for x in tab2_content:
        rs = x.text
        name = rs.split()[2]
        if name not in t2 and name not in t1:  # rs.find('завершена') != -1 если не закончилась
            if rs.find('завершена') != -1:
                rs = rs[:rs.find('регистрация') - 1]
            time = ' '.join(rs.split()[:2])
            name = ' '.join(rs.split()[2:])
            ans1.append((time, name))

    tab3 = tab_bs.find_all('div', id='tabs-3')
    tab3_content = [v.find_all('h3') for v in tab3][0]
    for x in tab3_content:
        rs = x.text
        name = rs.split()[2]
        if name not in t2 and name in t1:  # rs.find('завершена') != -1 если не закончилась
            if rs.find('завершена') != -1:
                rs = rs[:rs.find('регистрация') - 1]
            time = ' '.join(rs.split()[:2])
            name = ' '.join(rs.split()[2:])
            ans2.append((time, name))

    ans = {'Надежда энергетики': {'Ссылка': 'https://www.energy-hope.ru', 'Отборочные': ans1, 'Заключительные': ans2}}

    return ans


