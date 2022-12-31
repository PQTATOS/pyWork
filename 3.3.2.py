import csv

compile = {}

with open('compile.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        compile[tuple(row[0].split('-'))] = {k: v for k, v in zip(header, row)}


with open('vacancies_dif_currencies.csv', encoding='utf-8-sig') as rF, open('new_file.csv', 'w', encoding='utf-8-sig', newline='') as wF:

    writer = csv.writer(wF)
    reader = csv.reader(rF)
    head = next(reader)
    new_head = ['name', 'salary', 'area_name', 'published_at']
    writer.writerow(new_head)
    for row in reader:
        d = {k: v for k, v in zip(head, row)}
        year, month = d['published_at'].split('-')[:2]
        curr_val = compile[year, month]
        new_row = []
        salary = ''
        if (d['salary_from'] != '' or d['salary_to'] != '') and (d['salary_currency'] == "RUR" or (d['salary_currency'] in curr_val and curr_val[d['salary_currency']] != '')):
            salary = 0
            count = 0
            if d['salary_from'] != '':
                salary += float(d['salary_from'])
                count += 1
            if d['salary_to'] != '':
                salary += float(d['salary_to'])
                count += 1
            currency = d['salary_currency']
            if currency != 'RUR':
                salary *= float(curr_val[currency])
            salary //= count

        for k in new_head:
            if k == 'salary':
                new_row.append(salary)
            else:
                new_row.append(d[k])

        writer.writerow(new_row)
