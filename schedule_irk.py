import requests as r
from bs4 import BeautifulSoup

types = {
           'schcls-item-distype type-1' : 'лекция',
           'schcls-item-distype type-2' : 'практика',
           'schcls-item-distype type-3' : 'лабораторная работа'
         }

class ScheduleParser():
    def __init__(self):
        
        site = r.get('https://www.istu.edu/raspisanie/grup/478232')

        finder = BeautifulSoup(site.text, 'html.parser')
        days = finder.find_all('div', 'sch-list-day')

        self.schedule = {}
        
        for day in days:
            day_of_week = day.find('h2', 'sch-list-day-header').text.split(', ')[0]
            #print(day_of_week)
            self.schedule[day_of_week] = {}
            
            subjects = day.find_all('div', 'sch-list-item')
            for sub in subjects:
                time = sub.find('div', 'sch-list-item-time-inner').text
                name = sub.find('div', 'schcls-item-name').text
                teacher = sub.find('div', 'schcls-item-prepod').text
                group = sub.find('div', 'schcls-item-group').text
                place = sub.find('div', 'schcls-item-aud').text

                lesson_type = 'Отсутсвует'

                for t in types.keys():
                    if sub.find('div', t) == None:
                        continue

                    lesson_type = types[t]

                self.schedule[day_of_week][name] = {}
                self.schedule[day_of_week][name]['name'] = name
                self.schedule[day_of_week][name]['time'] = time
                self.schedule[day_of_week][name]['type'] = lesson_type
                self.schedule[day_of_week][name]['teacher'] = teacher
                self.schedule[day_of_week][name]['group'] = group
                self.schedule[day_of_week][name]['place'] = place

                #print(self.schedule[day_of_week][name])

sch = ScheduleParser()

print(sch.schedule['Пятница'].keys())