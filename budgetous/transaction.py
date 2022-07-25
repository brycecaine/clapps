import sqlite3


from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

entries = [
    '23.43 DI',
    '14.57 Mo Bettahs',
    '34.98 Costco 6/21/2022',
    '46.00 Jun 30 Xfinity',
    '18.23',
    '13',
    '32.76 yesterday',
    '53.19 Jul 20',
]

def get_date_from_list(items):
    dt = None

    for item in items:
        try:
            dt = parse(item)
            break
        except ParserError:
            dt = datetime.now()

    return dt
        

def get_dt_from_details(details):
    if 'today' in details:
        dt = datetime.now()

    elif 'yesterday' in details:
        print('why')
        dt = datetime.now() - timedelta(days=1)

    else:
        try:
            dt = parse(details)
        except ParserError:
            parts = details.split(' ')
            dt = get_date_from_list(parts)

            if dt is None:
                dt = datetime.now()

    return dt


def get_vendor_id_from_details(details):
    vendor_id = None

    details_parts = details.split(' ')

    conn = sqlite3.connect('budgetous.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    stmt = 'select id, name from vendor'

    results = cur.execute(stmt).fetchall()


    '''
    vendors = []
    for result in results:
        vendors.append(result['name'])
    '''

    vendors = [result['name'] for result in results]

    vendor_name = None

    for vendor in vendors:
        if vendor in details:
            vendor_name = vendor

    vendors_set = set(vendors)
    details_parts_set = set(details_parts)
    intersection_set = details_parts_set.intersection(vendors_set)

    if intersection_set:
        # Assumes only one vendor allowed in entry
        vendor_name = list(intersection_set)[0]

    vendor_ids = [
        result['id']
        for result in results
        if result['name'] == vendor_name]

    vendor_id = None

    if vendor_ids:
        vendor_id = vendor_ids[0]

    conn.close()

    return vendor_id


def parse_transaction(entry):
    tx = {}
    print('--------------------')
    print(f'{entry}')
    parts = entry.split(' ')
    amount = parts.pop(0)
    details = ' '.join(parts)  # details are everything other than the amount

    vendor_id = get_vendor_id_from_details(details)
    dt = get_dt_from_details(details)

    tx = {
        'amount': amount,
        'vendor_id': vendor_id,
        'dt': dt,
        'account_id': 3,
        'entry': entry,
        'file_path': '/wef/wef/wef',
    }

    print(tx)

    return tx


def insert_entry_into_db(entry):
    # TODO: check if tx already exists
    conn = sqlite3.connect('budgetous.db')
    cur = conn.cursor()

    tx = parse_transaction(entry)

    tx_keys = ','.join(tx.keys())
    tx_param_fields = ','.join([f':{key}' for key, val in tx.items()])

    stmt = f'''
        insert into tx ({tx_keys}) values ({tx_param_fields})
    '''

    cur.execute(stmt, tx)

    conn.commit()
    conn.close()


for entry in entries:
    insert_entry_into_db(entry)

