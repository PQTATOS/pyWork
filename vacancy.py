
            return vacs


if input("Введите данные для печати(Вакансии/Статистика): ") == "Статистика":
    os.startfile("statistic.py")
else:
<<<<<<< HEAD
    fileName_ = input("Введите название файла: ")
=======
    file_Name = input("Введите название файла: ")
>>>>>>> develop

    inputs = InputConect()
    inputs.addFilter(input("Введите параметр фильтрации: "))
    inputs.addSort(input("Введите параметр сортировки: "))
    inputs.addReverse(input("Обратный порядок сортировки (Да / Нет): "))
    inputs.addStartEnd(input("Введите диапазон вывода: "))
    inputs.addFieldsToPrint(input("Введите требуемые столбцы: "))

    if not inputs.IsCorrect:
        print(inputs.WrongLine)
    else:
        vacs = DataSet(fileName)
        inputs.print_VacanciesTable(vacs)
inputs.print_VacanciesTable(vacs)
