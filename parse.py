import requests, time, lxml
from bs4 import BeautifulSoup as BS
from requests.exceptions import HTTPError

def get_schedule(group):
    group = str(group)

    site = 'https://www.bsu.edu.ru/bsu/resource/schedule/groups/index.php?group=' + group
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36 OPR/66.0.3515.75',
        'Cookie': '_ym_uid=1522696719275410740; BX_USER_ID=a958801090decbe5263bfc6906d61e04; _ga=GA1.3.1238018391.1530212756; __utmz=144657958.1555879377.7.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); BITRIX_SM_LAST_ADV=5; _ym_d=1567077526; __utmc=144657958; BITRIX_SM_GUEST_ID=76406761; _ym_isad=2; _ym_visorc_44155434=w; __utma=144657958.1238018391.1530212756.1582139974.1582142314.34; __utmt=1; __utmb=144657958.2.10.1582142314; PHPSESSID=Q0KhTvmyH9Huiya4vvGe4HLnkhFNVVP2; BITRIX_SM_LAST_VISIT=19.02.2020+23%3A04%3A19',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

    for url in [site]:
        try:
            response = requests.get(url, headers=headers) # Заходим на сайт для получения номера недели
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP ошибка: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Другая ошибка: {err}')  # Python 3.6
        else:
            print('Успешно!')

    html = BS(response.content, 'lxml') # находим поле с неделей
    week = html.find('span', id='week')
    week = week.get('name')


    schedule_site = 'https://www.bsu.edu.ru/bsu/resource/schedule/groups/show_schedule.php?group={}&week={}'.format(group, week)

    response_schedule = requests.get(schedule_site, headers=headers) # Заходим на сайт который отдает расписание на запрос с группой
    response_schedule.raise_for_status()
    day_html = BS(response_schedule.content, 'html.parser')  # Парсим страницу
    date_td = day_html.find_all('b')
    times_td = day_html.find_all('td', id='time')  # Получаем таблицу времени
    lessons_td = day_html.find_all('td', id='lesson')  # Получаем таблицу предметов
    teachers_td = day_html.find_all('td', id='teacher')  # получаем таблицу учителей
    aud_td = day_html.find_all('td', id='aud')  # Получаем массив аудиторий
    les_type = 0
    les_name = 1
    date = []
    times = []
    lessons = []
    teachers = []
    aud = []
    day = 0
    for i in range(len(date_td)):  # Заполняем массив дат
        date.append(date_td[i].text.replace('\n', ''))
    for i in range(len(times_td)):  # Заполняем массив времени
        times.append(times_td[i].text.replace('\n', ''))
        if times_td[i].get('rowspan') == '2':
            times.append(times_td[i].text.replace('\n', ''))
    for i in range(len(aud_td)):  # Формируем массивы предмета, преподавателя и аудитории
        lessons.append(
            lessons_td[les_type].text.replace('  ', '').replace('\n', '') + lessons_td[les_name].text.replace('  ',
                                                                                                              '').replace(
                '\n', ''))
        teachers.append(teachers_td[i].text.replace('  ', '').replace('\n', ''))
        aud.append(aud_td[i].text.replace('  ', '').replace('\n', ''))
        les_type += 2
        les_name += 2
    i = 0
    days = [[] * 1 for i in range(len(date))]
    for day in date:
        while True:
            days[date.index(day)].append('*' + times[i] + '*' + ' || ' + aud[i] + '\n' + '-------' + '\n' + lessons[i] + '\n' + teachers[i] + '\n')
            if i == (len(lessons)-1):
                break
            if int(times[i].replace(' ', '').replace(':', '').replace('-', '')) > int(times[i+1].replace(' ', '').replace(':', '').replace('-', '')):
                i += 1
                break
            i += 1
    return days, date