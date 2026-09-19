import io
from math import ceil
import openpyxl
import requests as r

# словарь для определения дня недели
days = {
    1 : 'Понедельник',
    2 : 'Вторник',
    3 : 'Среда',
    4 : 'Четверг',
    5 : 'Пятница',
    6 : 'Суббота'
}

class ScheduleParserMsk():
    def __init__(self):
        # инструменты поиска
        self.file_id = '1yeUrQ27LC8yHmlXE7ZWzEcEkDVa2mgyP1T4FS42JTMQ'
        self.gid = '1164699216'

        self.url = f'https://docs.google.com/spreadsheets/d/{self.file_id}/export?format=xlsx&gid={self.gid}'

    # функция перевода из московоского времени в иркутское
    def msk_to_irk(self, time):
        irk_time = [] # составные части для записи времени

        for t in time.split('-'): # разделение времени начала и конца пары на отедльные объекты 
            parts_of_time = t.split(':') # разделение по часам и минутам

            hh = str(int(parts_of_time[0]) + 5) # добавление разницы во времени
            mm = parts_of_time[1]

            irk_time.append(':'.join([hh, mm])) # запись в формате hh:mm

        return '-'.join(irk_time) # соеденение времени в промежуток

    # функция определения расписания
    def find(self):
        # обработка исходных данных
        self.res = r.get(self.url)
        self.sheet = openpyxl.load_workbook(io.BytesIO(self.res.content)).active

        
        self.schedule = {} # создание основоного словаря для хранениях данных расписания

        count = 1 # счётчик строк таблицы

        # перебор строк в таблице расписания
        for row in self.sheet.iter_rows(min_col=1, max_col=4, min_row=2, max_row=49):
                # переход на новую строку
                count += 1

                subj_inf_txt = row[3].value # определение информации о паре

                if subj_inf_txt == None:
                    continue

                day = days[ceil((count - 1) / 8)] # определение дня

                # форматирование полученной информации для дальнейшего разделения
                subj_inf_txt = subj_inf_txt.strip()
                subj_inf_txt = subj_inf_txt.replace('\n', ', ')
                subj_inf_txt = subj_inf_txt.replace(')', '')
                subj_inf = subj_inf_txt.split(' (')

                # опредление типа пары (лекция, практика, лаборатная работа)
                if ', ' in subj_inf_txt:
                    subj_name = subj_inf[0].split(', ')[0]
                    subj_type = subj_inf[0].split(', ')[1]
                else:
                    subj_name = subj_inf[0]
                    subj_type = 'семинар + лекция'

                # запись данных о паре
                time = subj_inf[1]

                if self.schedule.get(day) == None:
                        self.schedule[day] = {}

                self.schedule[day][subj_name] = {}
                    
                self.schedule[day][subj_name]['time irk'] = self.msk_to_irk(time)
                self.schedule[day][subj_name]['time msk'] = time
                self.schedule[day][subj_name]['type'] = subj_type
                self.schedule[day][subj_name]['name'] = subj_name
