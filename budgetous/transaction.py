from decimal import Decimal
import numbers
import sqlite3

from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

VENDORS = [
    'DI',
    'Mo Bettahs',
    'Costco',
]
CATEGORIES = [
    'Groceries',
    'Clothes',
]
TAGS = [
    'follow-up',
    'reimbursable',
]

entries = [
    # '23.43 DI',
    # '14.57 Mo Bettahs',
    # '34.98 Costco Groceries 6/21/2022',
    # '46.00 Jun 30 Xfinity',
    # '18.23 reimbursable',
    # '13',
    # '32.76 yesterday',
    # '53.19 Jul 20',
    '42 split Groceries 20 Clothes 22',
]


def get_dt_from_list(items):
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
        dt = datetime.now() - timedelta(days=1)

    else:
        try:
            dt = parse(details)
        except ParserError:
            parts = details.split(' ')
            dt = get_dt_from_list(parts)

            if dt is None:
                dt = datetime.now()

    return dt


def get_vendor(entry):
    return_val = None

    for vendor in VENDORS:
        if vendor in entry:
            return_val = vendor
            break

    return return_val


def items_in_list(items, main_list, return_type):
    main_list_set = set(main_list)
    items_set = set(items)
    intersection_set = items_set.intersection(main_list_set)
    common_items = list(intersection_set)

    if return_type == 'one':
        try:
            return_val = common_items[0]

        except IndexError:
            return_val = None

    else:
        return_val = common_items

    return return_val


def list_to_dict(list_in):
    itr = iter(list_in)
    res_dct = dict(zip(itr, itr))

    return res_dct


def get_split_parts(parts):
    split_parts = {}

    try:
        idx = parts.index('split')

        split_parts = list_to_dict(parts[idx+1:])

    except ValueError:
        pass

    return split_parts


def parse_txs(entry):
    tx = {}
    parts = entry.split(' ')
    amount = parts.pop(0)
    details = ' '.join(parts)  # details are everything other than the amount

    vendor = get_vendor(entry)
    dt = get_dt_from_details(details)
    tags = ' '.join(items_in_list(parts, TAGS, 'all'))

    txs = []

    split_parts = get_split_parts(parts)

    if split_parts:
        for i, split_part in enumerate(split_parts.items(), 1):
            key, val = split_part

            if key in CATEGORIES:
                val_num = float(val)
                tx = {
                    'amount': val_num,
                    'vendor': vendor,
                    'dt': dt,
                    'category': key,
                    'tags': tags,
                    'account_id': 3,
                    'seq_no': i,
                    'entry': entry,
                    'file_path': '/wef/wef/wef',
                }
                txs.append(tx)
    else:
        category = items_in_list(parts, CATEGORIES, 'one')
        tx = {
            'amount': amount,
            'vendor': vendor,
            'dt': dt,
            'category': category,
            'tags': tags,
            'account_id': 3,
            'seq_no': 1,
            'entry': entry,
            'file_path': '/wef/wef/wef',
        }
        txs.append(tx)

    return txs


def get_where_clause(table_name, record):
    where_clause_expressions = []
    
    for k, v in record.items():
        comparator = '=' if v is not None else 'is'
        where_clause_expression = f'and {k} {comparator} :{k}'
        where_clause_expressions.append(where_clause_expression)

    where_clause = ' '.join(where_clause_expressions)
    where_clause = where_clause.replace('and', 'where', 1)

    return where_clause


def exists_in_db(table_name, record):
    where_clause = get_where_clause(table_name, record)
    sql = f'select * from {table_name} {where_clause}'

    conn = sqlite3.connect('budgetous.db')
    cur = conn.cursor()
    cur.execute(sql, record)

    exists = len(cur.fetchall()) > 0

    conn.commit()
    conn.close()

    return exists
    

def insert_entry_into_db(entry):
    conn = sqlite3.connect('budgetous.db')
    cur = conn.cursor()

    txs = parse_txs(entry)

    tx_keys = ','.join(txs[0].keys())

    for tx in txs:
        tx_param_fields = ','.join([f':{key}' for key, val in tx.items()])

        if not exists_in_db('tx', tx):
            stmt = f'insert into tx ({tx_keys}) values ({tx_param_fields})'
            cur.execute(stmt, tx)

    conn.commit()
    conn.close()


for entry in entries:
    print(entry)
    insert_entry_into_db(entry)
