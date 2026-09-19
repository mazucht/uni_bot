from bs4 import BeautifulSoup
import requests as r

# все лекций и их классы
types = {
           'schcls-item-distype type-1' : 'лекция',
           'schcls-item-distype type-2' : 'практика',
           'schcls-item-distype type-3' : 'лабораторная работа'
         }

class ScheduleParserIrk():
    def __init__(self):
        # инструменты поиска
        self.site = r.get('https://www.istu.edu/raspisanie/grup/478232')
        self.finder = BeautifulSoup(self.site.text, 'html.parser')

    def find(self):
        # информация о всех днях рабочей недели
        days = self.finder.find_all('div', 'sch-list-day')

        # создание основного словаря для хранения данных расписания
        self.schedule = {}

        # перебор информации о каждом рабочем дне
        for day in days:
            # какой рабочий день обрабатывается
            day_of_week = day.find('h2', 'sch-list-day-header').text.split(', ')[0]

            # организация места хранения информации о рабочем дне
            self.schedule[day_of_week] = {}

            # поиск всей информации по парам
            subjects = day.find_all('div', 'sch-list-item')

            # перебор информации по каждому предмету
            for sub in subjects:
                # извлечение необходимой информации
                time = sub.find('div', 'sch-list-item-time-inner').text
                name = sub.find('div', 'schcls-item-name').text
                teacher = sub.find('div', 'schcls-item-prepod').text
                group = sub.find('div', 'schcls-item-group').text
                place = sub.find('div', 'schcls-item-aud').text

                # определение типа пары
                lesson_type = 'Отсутсвует'

                for t in types.keys():
                    if sub.find('div', t) == None:
                        continue

                    lesson_type = types[t]

                # оргаенизвция места хранения инормации о паре
                self.schedule[day_of_week][name] = {}

                # запись данных о паре
                self.schedule[day_of_week][name]['name'] = name
                self.schedule[day_of_week][name]['time'] = time
                self.schedule[day_of_week][name]['type'] = lesson_type
                self.schedule[day_of_week][name]['teacher'] = teacher
                self.schedule[day_of_week][name]['group'] = group
                self.schedule[day_of_week][name]['place'] = place
