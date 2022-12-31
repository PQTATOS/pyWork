import csv
import decimal
import requests
import xml.etree.ElementTree as ET

def get_freq_and_minmax_date(file_name):
    dict = {}
    min_date = [2023, 12]
    max_date = [2000, 12]
    with open(file_name, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[3] not in dict:
                dict[row[3]] = 0
            dict[row[3]] += 1
            date = list(map(int, row[5][:10].split('-')))
            if date[0] < min_date[0]:
                min_date = date
            elif date[0] == min_date[0] and date[1] < min_date[1]:
                min_date = date


            if date[0] > max_date[0]:
                max_date = date
            elif date[0] == max_date[0] and date[1] > max_date[1]:
                max_date = date

    return (dict, min_date, max_date)

def get_value(min_date, max_date):
    for year in range(min_date[0], max_date[0] + 1):
        for month in range(1, 13):
            response = requests.get(f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{month:02}/{year}')
            with open(f'currency_by_year/{month}-{year}.xml', 'w') as f:
                f.write(response.text)

def make_database(currencies, min_date, max_date):
    with open('compile.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date'] + currencies)
        for year in range(min_date[0], max_date[0] + 1):
            for month in range(1, 13):
                if year == max_date[0] and month > max_date[1]:
                    break
                if year == min_date[0] and month < min_date[1]:
                    continue
                tree = ET.parse(f'currency_by_year/{month}-{year}.xml')
                row = [f'{year}-{month:02}']
                for curr in currencies:
                    value = tree.find(f"Valute[CharCode='{curr}']/Value")
                    if value != None:
                        row.append(decimal.Decimal(value.text.replace(',', '.')) / int(
                            tree.find(f"Valute[CharCode='{curr}']/Nominal").text))
                    else:
                        row.append('')
                writer.writerow(row)

cur, min_date, max_date = get_freq_and_minmax_date('vacancies_dif_currencies.csv')

cur = list(filter(lambda x: cur[x] > 5000 and x != '' and x !='RUR', cur))

make_database(cur, min_date, max_date)