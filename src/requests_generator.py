import re
import language_processing


def parse_purpose(purpose, values_for_names, values_for_fees):
    phone = ''
    for m in re.finditer(r"((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", purpose):
        # Check for phone number, not date or something else.
        if m.group().startswith('8') or m.group().startswith('+7') or m.group().startswith('7'):
            phone = m.group()  # Nothing.

    email = ''
    for word in purpose.split():
        if '@' in word:
            email = word

    B24_ID = ''
    patient_id = ''
    names = language_processing.select_names('.' + purpose + '.')  # . is magic.
    for name in names:
        for name_part in name.values():
            if name_part in values_for_names.keys():
                patient_id = values_for_names[name_part][0]
                B24_ID = int(values_for_names[name_part][1])

    TARGET = ''
    fundraiser_id = ''
    fundraiser_name = ''
    PAY = 'Да'
    if B24_ID:
        fundraiser_id = values_for_fees[B24_ID][3]
        fundraiser_name = values_for_fees[B24_ID][0]
        TARGET = values_for_fees[B24_ID][2]

    return phone, email, B24_ID, patient_id, TARGET, fundraiser_id, fundraiser_name, PAY


def generate_requests_csv(clear_data, values_for_names, values_for_fees):
    start_id = 200000


    output = 'IE_XML_ID;IE_NAME;IE_ID;IE_ACTIVE_FROM;IE_ACTIVE_TO;IE_PREVIEW_PICTURE;IE_PREVIEW_TEXT;IE_PREVIEW_TEXT_TYPE;IE_DETAIL_PICTURE;IE_DETAIL_TEXT;IE_DETAIL_TEXT_TYPE;IE_CODE;IE_SORT;IE_TAGS;IP_PROP238;IP_PROP12;IP_PROP5;IP_PROP236;IP_PROP6;IP_PROP10;IP_PROP239;IP_PROP234;IP_PROP2;IP_PROP11;IP_PROP8;IP_PROP7;IP_PROP13;IP_PROP3;IP_PROP4;IP_PROP1;IP_PROP235;IP_PROP9;IC_GROUP0;IC_GROUP1;IC_GROUP2\n'

    for n, transaction in enumerate(clear_data):
        purpose = transaction['НазначениеПлатежа'].replace(';', ' ').replace(',', ' ')

        phone, email, B24_ID, patient_id, TARGET, fundraiser_id, fundraiser_name, PAY = parse_purpose(purpose,
                                                                                                      values_for_names,
                                                                                                      values_for_fees)
        payment_type = 'CloudPayments'

        data = [start_id + n, transaction['Плательщик'], start_id + n,
                '', '', '', '', 'text', '', '', 'text', email,
                '500', '', patient_id, '', '', TARGET, '', fundraiser_id, '', fundraiser_name, 'Да', 'Да', payment_type, '',
                '', '',
                ''.join(transaction['Сумма'].split('.')[:1]), phone, '', '', '', '', '\n']
        output += ';'.join(str(i) for i in data)

    return output

    # transaction['Дата'].replace('.', '-') + ' 00:00:00'
