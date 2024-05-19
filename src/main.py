import parser
import filter
import server_communication
import requests_generator
import os

if 'main.py' in os.listdir(path='.'):  # Strange error - run from /data or not.
    os.chdir('..')

last_date = parser.get_last_date()
print('Last parsed date:', last_date)
raw_data = parser.parse_all_files(last_date)

clear_data = filter.filter(raw_data)

print('Transaction count before and after filtering:', len(raw_data), len(clear_data))

values_for_names = server_communication.get_names()
values_for_fees = server_communication.get_fees()

with open('requests.csv', mode='w', encoding='UTF-8') as file_output:
    requests = requests_generator.generate_requests_csv(clear_data, values_for_names, values_for_fees)
    file_output.write(requests)