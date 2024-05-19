from datetime import datetime
import os


def read_time(time_str: str):
    return datetime.strptime(time_str, "%d.%m.%Y")


def get_last_date(working_dir_path="data/"):
    try:
        with open(working_dir_path + 'last_date', mode='r') as lastdate_file:
            last_date = read_time(lastdate_file.readline())
    except (FileNotFoundError, ValueError):
        print('last_date file does not exist!')
        last_date = read_time('01.01.2000')

    return last_date


def set_last_date(date: datetime, working_dir_path="data/"):
    with open(working_dir_path + 'last_date', mode='w') as lastdate_file:
        lastdate_file.write(date.strftime("%d.%m.%Y"))


def parse_all_files(last_date: datetime, working_dir_path="data/"):
    documents = []  # Values to return.

    os.chdir(working_dir_path)
    filenames = os.listdir(path='.')
    os.chdir('..')

    for filename in filenames:
        if not filename.endswith('.txt'):
            print('"' + filename + '"', 'is not a upload file. Skipped.')
            continue

        with open(working_dir_path + filename, mode='r', encoding='UTF-8') as file:
            # Reading file information and date.
            parameters = dict()
            while buff := file.readline().rstrip():
                if '=' in buff:  # Check for parameter=value.
                    parameter, value = buff.split('=')

                    parameters[parameter] = value

            try:
                creation_date = read_time(parameters['ДатаСоздания'])
                start_date = read_time(parameters['ДатаНачала'])
                end_date = read_time(parameters['ДатаКонца'])
            except KeyError:
                print('Ошибка при чтении заголовка файла!')
                continue

            if start_date <= last_date:
                print(filename, 'ends before last_date! Skipped.')
                continue

            # Reading documents blocks.
            in_document = False
            while True:
                buff = file.readline().rstrip()

                if buff.startswith('КонецФайла'):
                    break
                elif buff.startswith('СекцияДокумент'):
                    in_document = True
                    parameters = dict()
                    # print('Начало')
                elif buff.startswith('КонецДокумента'):
                    in_document = False
                    documents.append(parameters)
                    # print('Конец')
                elif buff and in_document:
                    try:
                        parameter, value = buff.split('=')
                        parameters[parameter] = value
                    except ValueError as error:
                        print('Error when reading', buff)

            set_last_date(end_date)

    return documents