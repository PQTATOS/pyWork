import math
import os
from prettytable import PrettyTable, ALL
import csv
import re


class DataSet:
    def __init__(self, _file_name):
        self.file_name = _file_name
        self.vacancies_objects = []
        if os.stat(_file_name).st_size == 0:
            print("Пустой файл")
            exit()
        self.csv_reader(self.file_name)

    def csv_reader(self, file_name):
        keys = []
        with open(file_name, newline='', encoding='utf-8-sig') as File:
            reader = csv.reader(File, delimiter=',')
            for row in reader:
                if not keys:
                    keys = row
                else:
                    if len(keys) != len(row) or row.__contains__(""):
                        continue
                    else:
                        self.vacancies_objects.append(Vacancy(self.csv_filer(row, keys)))
            if len(self.vacancies_objects) == 0:
                print("Нет данных")
                exit()

    def csv_filer(self, row, keys):
        for index in range(len(row)):
            row[index] = re.sub(r'<[^>]+>', "", row[index]).split("\n")
            for i in range(len(row[index])):
                row[index][i] = re.sub(r'\s+', " ", row[index][i]).strip()
            if keys[index] == 'key_skills':
                row[index] = row[index]
            else:
                row[index] = row[index][0]
        return row


class Vacancy:
    def __init__(self, row):
        self.name = row[0]
        self.description = row[1]
        self.key_skills = row[2]
        self.experience_id = row[3]
        self.premium = row[4]
        self.employer_name = row[5]
        self.salary = Salary(row)
        self.area_name = row[10]
        self.published_at = row[11]

    def returnValue(self, field):
        return {'name': self.name, 'description': self.description, 'key_skills': self.key_skills,
                'experience_id': self.experience_id, 'premium': self.premium, 'employer_name': self.employer_name,
                'salary': self.salary, 'area_name': self.area_name, 'published_at': self.published_at
               }[field]


class Salary:
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    def __init__(self, row):
        self.salary_from = row[6]
        self.salary_to = row[7]
        self.salary_gross = row[8]
        self.salary_currency = row[9]

    def covertToRub(self, str):
        if str == "to":
            return float(self.salary_to) * self.currency_to_rub[self.salary_currency]
        else:
            return float(self.salary_from) * self.currency_to_rub[self.salary_currency]


class InputConect:
    inverted_dic = {'Название': 'name', 'Описание': 'description', 'Навыки': 'key_skills',
                    'Опыт работы': 'experience_id',
                    'Премиум-вакансия': 'premium', 'Компания': 'employer_name',
                    'Нижняя граница вилки оклада': 'salary_from',
                    'Верхняя граница вилки оклада': 'salary_to', 'Оклад указан до вычета налогов': 'salary_gross',
                    'Идентификатор валюты оклада': 'salary_currency', 'Название региона': 'area_name',
                    'Дата публикации вакансии': 'published_at', 'Оклад': 'salary'}
    rus_naming = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
                "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары",
                "UZS": "Узбекский сум", "True": "Без вычета налогов", "False": "С вычетом налогов"}

    def __init__(self):
        self.IsCorrect = True
        self.WrongLine = ''
        self.filter_param = []
        self.sort_param = ''
        self.IsReverse = False
        self.startEnd = ''
        self.fieldsToPrint = ''

    def addFilter(self, filter):
        if filter == "":
            return
        elif not filter.__contains__(': '):
            self.IsCorrect = False
            self.WrongLine = "Формат ввода некорректен"
            return

        filter = filter.split(": ")
        if filter[0] not in self.inverted_dic:
            self.IsCorrect = False
            self.WrongLine = "Параметр поиска некорректен"
            return
        self.filter_param.append(self.inverted_dic[filter[0]])
        if filter[0] in ['Идентификатор валюты оклада', 'Оклад указан до вычета налогов', 'Премиум-вакансия','Опыт работы']:
            self.filter_param.append({"Да": "True", "Нет": "False", "Без вычета налогов": "True", "С вычетом налогов": "False",
                                    "Нет опыта": "noExperience", "От 1 года до 3 лет": "between1And3", "От 3 до 6 лет": "between3And6",
                                    "Более 6 лет": "moreThan6", "Манаты": "AZN", "Белорусские рубли": "BYR",
                                    "Евро": "EUR", "Грузинский лари": "GEL", "Киргизский сом": "KGS", "Тенге": "KZT",
                                    "Рубли": "RUR", "Гривны": "UAH", "Доллары": "USD", "Узбекский сум": "UZS"
                                    }[filter[1]])
        else:
            self.filter_param.append(filter[1])

    def addSort(self, sort):
        if sort == "":
            return
        if sort not in self.inverted_dic:
            self.WrongLine = "Параметр сортировки некорректен"
            self.IsCorrect = False
            return
        self.sort_param = self.inverted_dic[sort]

    def addReverse(self, str):
        if str not in ["Да", "Нет", ""]:
            self.WrongLine = "Порядок сортировки задан некорректно"
            self.IsCorrect = False
            return
        self.IsReverse = str == 'Да'

    def addStartEnd(self, str):
        self.startEnd = str.split()

    def addFieldsToPrint(self, str):
        self.fieldsToPrint = str.split(', ')

    def int_form(self, digit):
        digit = (lambda x: x[:-2] if x[-2:] == '.0' else x)(digit)

        prevT = 0
        curT = (lambda x: 3 if x == 0 else x)(int(len(digit) % 3))
        new_dig = ""
        if len(digit) == 3:
            return str(digit)
        for i in range(math.ceil(len(digit) / 3)):
            if i == 0:
                new_dig += digit[:curT]
            else:
                new_dig += " " + digit[prevT:curT]
            prevT = curT
            curT += 3

        return new_dig

    def date_form(self, date):
        return f"{date[8:10]}.{date[5:7]}.{date[:4]}"

    def MakeVacanciesTable(self, data):
        vacs = self.vac_filter(data.vacancies_objects)
        if len(vacs) == 0:
            print("Ничего не найдено")
            exit()
        vacs = self.sorter(vacs)

        mt = PrettyTable()
        mt.align = "l"
        mt.hrules = ALL

        for index in range(len(vacs)):
            newVacDict = self.formatter(vacs[index])
            if len(mt.field_names) == 0:
                mt.field_names = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания",
                                  "Оклад", "Название региона", "Дата публикации вакансии"]

            mt.add_row([index + 1, newVacDict["Название"], newVacDict["Описание"], newVacDict["Навыки"],
                        newVacDict["Опыт работы"], newVacDict["Премиум-вакансия"], newVacDict["Компания"],
                        newVacDict["Оклад"], newVacDict["Название региона"], newVacDict["Дата публикации вакансии"]])
        mt.max_width = 20
        return mt

    def print_VacanciesTable(self, data):
        table = self.MakeVacanciesTable(data)
        fields_print = (lambda x: table.field_names if x[0] == "" else ["№"] + x)(self.fieldsToPrint)

        if len(self.startEnd) == 2:
            print(table.get_string(start=int(self.startEnd[0]) - 1, end=int(self.startEnd[1]) - 1, fields=fields_print))
        elif len(self.startEnd) == 1:
            print(table.get_string(start=int(self.startEnd[0]) - 1, fields=fields_print))
        else:
            print(table.get_string(fields=fields_print))

    def formatter(self, vac):
        new_dict = {}
        if len(vac.returnValue('description')) > 100:
            new_dict["Описание"] = vac.returnValue('description')[:100] + '...'
        else:
            new_dict["Описание"] = vac.returnValue('description')

        x = '\n'.join(vac.returnValue('key_skills'))
        if len(x) > 100:
            new_dict["Навыки"] = x[:100] + '...'
        else:
            new_dict["Навыки"] = x

        new_dict["Название"] = vac.returnValue('name')
        new_dict["Опыт работы"] = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
                                   "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет"
                                   }[vac.returnValue('experience_id')]
        new_dict["Премиум-вакансия"] = {'False': 'Нет', 'True': 'Да'}[vac.returnValue('premium')]
        new_dict["Компания"] = vac.returnValue('employer_name')
        new_dict['Оклад'] = f'{self.int_form(vac.returnValue("salary").salary_from)} - {self.int_form(vac.returnValue("salary").salary_to)} '\
                            f'({self.rus_naming[vac.returnValue("salary").salary_currency]}) '\
                            f'({self.rus_naming[vac.returnValue("salary").salary_gross]})'
        new_dict["Название региона"] = vac.returnValue('area_name')
        new_dict["Дата публикации вакансии"] = self.date_form(vac.returnValue('published_at'))
        return new_dict

    def vac_filter(self, vacs):
        if len(self.filter_param) != 2:
            return vacs
        elif self.filter_param[0] == "salary":
            return [x for x in vacs if float(x.salary.salary_from) <= float(self.filter_param[1]) <= float(x.salary.salary_to)]
        elif self.filter_param[0] == 'salary_gross':
            return [x for x in vacs if x.salary.salary_gross == self.filter_param[1]]
        elif self.filter_param[0] == 'salary_currency':
            return [x for x in vacs if x.salary.salary_currency == self.filter_param[1]]
        elif self.filter_param[0] == "key_skills":
            self.filter_param[1] = self.filter_param[1].split(', ')
            return [x for x in vacs if all(y in x.key_skills for y in self.filter_param[1])]
        elif self.filter_param[0] == 'published_at':
            return [x for x in vacs if self.date_form(x.published_at) == self.filter_param[1]]
        else:
            return [x for x in vacs if x.returnValue(self.filter_param[0]) == self.filter_param[1]]

    def sorter(self, vacs):
        if self.sort_param == "":
            return vacs

        if self.sort_param in ['key_skills', 'experience_id', 'salary', 'published_at']:
            dic_sorter = {
                'key_skills': lambda x: len(x.returnValue('key_skills')),
                'experience_id':
                    lambda x: {"noExperience": 0, "between1And3": 1, "between3And6": 2, "moreThan6": 3}[
                        x.returnValue('experience_id')],
                'salary':
                    lambda x: (x.salary.covertToRub('from') + x.salary.covertToRub('to')) / 2,
                'published_at': lambda x: int(re.sub('[-T:+]', '', x.returnValue('published_at')))
            }
            vacs.sort(key=dic_sorter[self.sort_param], reverse=self.IsReverse)
            return vacs
        else:
            vacs.sort(key=lambda x: x.returnValue(self.sort_param), reverse=self.IsReverse)
            return vacs


if input("Введите данные для печати(Вакансии/Статистика): ") == "Статистика":
    os.startfile("statistic.py")
else:
    fileName_ = input("Введите название файла: ")

    inputs = InputConect()
    inputs.addFilter(input("Введите параметр фильтрации: "))
    inputs.addSort(input("Введите параметр сортировки: "))
    inputs.addReverse(input("Обратный порядок сортировки (Да / Нет): "))
    inputs.addStartEnd(input("Введите диапазон вывода: "))
    inputs.addFieldsToPrint(input("Введите требуемые столбцы: "))

    if not inputs.IsCorrect:
        print(inputs.WrongLine)
    else:
        vacs = DataSet(fileName_)
        inputs.print_VacanciesTable(vacs)
