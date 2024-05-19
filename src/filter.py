def filter(raw_data: list):
    condition_file = 'src/condition.txt'

    #импут переменных из файла
    with open(condition_file, 'r') as file:
        INN_P = file.readline().strip()
        Plat_1 = file.readline().strip()
        Plat_2 = file.readline().strip()
        NaznPlat_1 = file.readline().strip()
        NaznPlat_2 = file.readline().strip()

    clear_data = []
    for i in raw_data:
        if i["ПлательщикИНН"] != INN_P:  # проверка на то, что это платеж

            if Plat_1 not in i["Плательщик"] \
                    and (Plat_2 not in i["Плательщик"] or NaznPlat_1 not in i["НазначениеПлатежа"]) \
                    and NaznPlat_2 not in i["НазначениеПлатежа"]:
                clear_data.append(i)
            else:
                print(i, 'thrown away!')
        else:
            print(i, 'thrown away fast!')

    return clear_data
