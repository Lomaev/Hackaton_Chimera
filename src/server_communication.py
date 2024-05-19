import requests
import language_processing


def _get_main_content(url: str):
    r = requests.post(url)

    start = r.text.find('<main')
    end = r.text.find('</main')

    return [tuple(i.split(';')) for i in r.text[start + 23:end].strip().split('<br>')[:-1]]  # 23 for opening <main> and empty lines.


def get_names():  # NAME, ID, B24_ID
    names_url = 'http://hackathon4.leikozu.net/test_get/'
    server_data = _get_main_content(names_url)
    values_for_names = dict()
    for NAME, ID, B24_ID in server_data:
        try:
            for processed_name in language_processing.select_names(NAME):
                # if one name for different people.
                if processed_name['first'] in values_for_names or processed_name['last'] in values_for_names:
                    print('Error, repeating name',  NAME + '!')
                    continue

                values_for_names[processed_name['first']] = (ID, B24_ID)
                values_for_names[processed_name['last']] = (ID, B24_ID)
        except Exception:  # Any exception.
            print('Error while processing name', NAME + '!')

    return values_for_names


def get_fees():  # B24_ID, NAME, PATIENT, ID, TARGET_ID
    names_url = 'http://hackathon4.leikozu.net/test_get_fees/'
    server_data = _get_main_content(names_url)
    values_for_fees = dict()
    for B24_ID, NAME, PATIENT, ID, TARGET_ID in server_data:
        values_for_fees[int(B24_ID)] = (NAME, PATIENT, ID, TARGET_ID)

    return values_for_fees