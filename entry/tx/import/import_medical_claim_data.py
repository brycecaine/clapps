import os
import csv
import sqlite3

ENTRY_DIR = os.environ['ENTRY_DIR']

COLUMN_NAMES = (
    'CLAIM_NUMBER',
    'CLAIM_DATE',
    'SUBSCRIBER_ID',
    'PATIENT_NAME',
    'PROVIDER_NAME',
    'PATIENT_DOB',
    'CLAIM_TYPE',
    'CLAIM_STATUS',
    'NETWORK_STATUS',
    'PROVIDER_TAX_ID',
    'SERVICE_BEGIN_DATE',
    'SERVICE_END_DATE',
    'PROCESSED_DATE',
    'PROCEDURE_CODE',
    'TYPE_OF_SERVICE',
    'AMOUNT_BILLED',
    'PROVIDER_DISCOUNT',
    'ALLOWABLE_AMOUNT',
    'AMOUNT_NOT_PAYABLE',
    'DEDUCTIBLE',
    'BENEFIT_PERCENTAGE_PAID_BY_PLAN',
    'OTHER_INSURANCE_PAID',
    'AMOUNT_PAID',
    'COPAY_AMOUNT',
    'PATIENT_RESPONSIBILITY',
    'MEDICAL_PAYMENT_DATE',
    'MEDICAL_PAYMENT_TO',
    'HRA_PAYMENT_DATE',
    'HRA_PAYMENT_TO',
)
 

try:
    with open('/Users/caine/Downloads/medical_claim_data.txt', 'r') as fin:
        dict_reader = csv.DictReader(fin, fieldnames=COLUMN_NAMES, delimiter='|')
        next(dict_reader)
        raw_records = list(dict_reader)
  
    record_dicts = []

    for record in raw_records:
        record_dict = {}

        for key, val in record.items():
            if key:
                record_dict[key] = val.replace('$', '')

        record_dicts.append(record_dict)

    conn = sqlite3.connect(f'{ENTRY_DIR}/entry.db')
    cursor = conn.cursor()
  
    column_names_str = ','.join(COLUMN_NAMES)
    parameter_names_str = ','.join([f':{column_name}' for column_name in COLUMN_NAMES])
    delete_sql = 'delete from medical_claim'
    insert_sql = (
        f'insert into medical_claim ({column_names_str}) values ({parameter_names_str})')
    cursor.execute(delete_sql)
    cursor.executemany(insert_sql, record_dicts)
  
    conn.commit()
    cursor.close()
  
except sqlite3.Error as error:
    print('Error occured: ', error)
  
finally:
    try:
        if conn:
            conn.close()
    except NameError:
        pass

