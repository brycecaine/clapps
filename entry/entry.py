from nltk import word_tokenize, pos_tag
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

import sys
import re
from decimal import Decimal
import numbers
import sqlite3

from datetime import datetime, timedelta, date
from dateutil.parser import parse
from dateutil.parser._parser import ParserError

VENDORS = [
    'DI',
    'Mo Bettahs',
    'Costco',
    'Xfinity',
]
CATEGORIES = [
    'Groceries',
    'Clothes',
    'Sleep',
]
TAGS = [
    'follow-up',
    'reimbursable',
]
MONTH_NUMBERS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
}


def get_vendor(entry):
    # docstring
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


def get_current_datetime(day_offset=0):
    dt = datetime(
        datetime.now().year, datetime.now().month,
        datetime.now().day+day_offset, 0, 0)

    return dt


def get_dates(entry, return_type='date'):
    dates = []

    if 'yesterday' in entry:
        yesterday = get_current_datetime(-1)
        dates.append(yesterday)

    if 'today' in entry:
        today = get_current_datetime()
        dates.append(today)

    if 'tomorrow' in entry:
        tomorrow = get_current_datetime(1)
        dates.append(tomorrow)

    year_pattern = r'(?P<year>[19|20]{2}[\d]{0,2})'
    month_digit_pattern = r'(?P<month>0?[1-9]|1[012])'
    # day_pattern = r'(?P<day>0?[1-9]|[12][0-9]|3[01])'
    day_pattern = r'(?P<day>[12][0-9]|3[01]|0?[1-9])'
    month_word_pattern = r'(?P<month_word>\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|(Nov|Dec)(?:ember)?))'

    patterns = {
        '%Y-%m-%d': f'{year_pattern}\-{month_digit_pattern}\-{day_pattern}',
        '%-m/%-d/%Y': f'{month_digit_pattern}\/{day_pattern}\/{year_pattern}',
        '%b %d %Y': f'{month_word_pattern}\s{day_pattern}\s?{year_pattern}?',
    }

    for format, pattern in patterns.items():
        matches = re.finditer(pattern, entry)

        for match in matches:
            date_dict = {}

            # Prepare dict to be passed to date()
            for key, val in match.groupdict().items():
                if val:
                    if val.isnumeric():
                        date_dict[key] = int(val)

                    elif key == 'month_word':
                        date_dict['month'] = MONTH_NUMBERS[val[0:3].lower()]

            if 'year' not in date_dict:
                date_dict['year'] = date.today().year

            if 'hour' not in date_dict:
                date_dict['hour'] = 0

            if 'minute' not in date_dict:
                date_dict['minute'] = 0

            date_obj = datetime(**date_dict)

            if return_type == 'str':
                dates.append(date_obj.strftime(format))
            else:
                dates.append(date_obj)

    return dates

    
def get_amount(entry, index=0):
    # pattern = r'\d+[\.^\/]?\d*'
    pattern = r'(?<!\d|/|-|\.|,)\d{1,}(?:\.\d{,2})?(?!\d|/|-|\.|,|:)'
    matches = re.findall(pattern, entry)
    entry_parts = entry.split(' ')

    if matches:
        amount = matches[index]
        amount_index = entry_parts.index(amount)

        try:
            prior_part = '' if index == 0 else entry_parts[amount_index-1]

        except IndexError:
            prior_part = ''

        try:
            next_part = entry_parts[amount_index+1]
        except IndexError:
            next_part = ''

        years = []
        years.extend(list(range(1950, 2100)))  # 4 digit years
        years.extend(list(range(0, 99)))  # 2 digit years
        years = [str(year) for year in years]
        months = [
            'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'oct', 'nov', 'dec',
        ]
        days = list(range(1, 32))
        days = [str(day) for day in days]

        if prior_part.lower() in months or next_part.lower() in years or prior_part.lower() in days:
            amount = float(get_amount(entry, index+1))
        else:
            amount = float(amount)

    else:
        parts = entry.split(' ')
        first_part = parts[0]

        if first_part.isnumeric():
            amount = float(first_part)

        else:
            amount = None

    return amount


def get_category(entry):
    entry_parts = entry.split(' ')
    categories = list(set(CATEGORIES).intersection(set(entry_parts)))
    category = categories[0] if categories else None

    return category


def is_tx(entry):
    is_transaction = True if get_amount(entry) else False

    return is_transaction


def get_present_tense_verb(entry):
    text = word_tokenize('I ' + entry)
    tagged_words = pos_tag(text)

    present_tense_verb = None

    if tagged_words[1][1] == 'VBP':
        present_tense_verb = tagged_words[1][0]

    return present_tense_verb


def is_todo(entry):
    present_tense_verb = get_present_tense_verb(entry)
    dates = get_dates(entry)

    is_td = False

    if present_tense_verb:
        today = get_current_datetime()

        for entry_date in dates:
            if entry_date >= today:
                is_td = True

        if not dates:
            is_td = True

    return is_td


def is_action(entry):
    dates = get_dates(entry)

    is_a = False

    if entry.split(' ')[0] in CATEGORIES:
        today = get_current_datetime()

        for entry_date in dates:
            if entry_date < today:
                is_a = True

        if not dates:
            is_a = True

    return is_a


def is_action_old(entry):
    category = get_category(entry)
    dates = get_dates(entry, return_type='str')
    
    entry_elements = entry.split(' ')
    action_elements = [category] + dates

    # An action is only a category and dates
    is_a = set(entry_elements) == set(action_elements)

    return is_a


def get_entry_type(entry):
    if entry == '':
        entry_type = None

    elif is_tx(entry):
        entry_type = 'transaction'

    elif is_action(entry):
        entry_type = 'action'

    elif is_todo(entry):
        entry_type = 'todo'

    else:
        entry_type = 'journal'

    return entry_type


def parse_txs(entry):
    parts = entry.split(' ')

    amount = get_amount(entry)
    vendor = get_vendor(entry)

    today = get_current_datetime()

    dts = get_dates(entry, return_type='date') or [today]
    dt = dts[0]

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


def get_where_clause(record):
    where_clause_expressions = []
    
    for k, v in record.items():
        comparator = '=' if v is not None else 'is'
        where_clause_expression = f'and {k} {comparator} :{k}'
        where_clause_expressions.append(where_clause_expression)

    where_clause = ' '.join(where_clause_expressions)
    where_clause = where_clause.replace('and', 'where', 1)

    return where_clause


def exists_in_db(table_name, record):
    where_clause = get_where_clause(record)
    sql_str = f'select * from {table_name} {where_clause}'

    results = run_sql(sql_str, params=record)

    exists = len(results) > 0

    return exists
    

def insert_tx_into_db(entry):
    txs = parse_txs(entry)

    tx_keys = ','.join(txs[0].keys())

    for tx in txs:
        tx_param_fields = ','.join([f':{key}' for key, val in tx.items()])

        if not exists_in_db('tx', tx):
            sql_str = f'insert into tx ({tx_keys}) values ({tx_param_fields})'
            run_sql(sql_str, params=tx)


def parse_action(entry):
    action = {}

    parts = entry.split(' ')

    action['category'] = get_category(entry)
    dates = get_dates(entry)

    try:
        action['dt_1'] = dates[0]
    except IndexError:
        action['dt_1'] = datetime.now()

    try:
        action['dt_2'] = dates[1]
    except IndexError:
        action['dt_2'] = ''

    return action


def insert_todo_into_file(entry):
    # Insert into orgzly file
    pass


def get_entry_db_conn():
    conn = sqlite3.connect('entry.db')

    return conn


def run_sql(sql_str, params=None):
    conn = get_entry_db_conn()

    cursor = conn.cursor()
    cursor.execute(sql_str, params)

    results = cursor.fetchall()

    conn.commit()
    conn.close()

    return results


def get_started_action(category):
    sql_str = ('select * '
               '  from action '
               ' where category = ? '
               '   and end_dt is null')

    results = run_sql(sql_str, (category,))

    started_action = results[0] if results else None

    return started_action


def insert_action_into_db(entry):
    action = parse_action(entry)

    started_action = get_started_action(action['category'])

    if not started_action:
        if not action['dt_2']:
            sql_str = ('insert '
                       '  into action '
                       '       (category, begin_dt) '
                       'values (?, ?)')

            params = (action['category'], action['dt_1'])

        else:
            sql_str = ('insert '
                       '  into action '
                       '       (category, begin_dt, end_dt) '
                       'values (?, ?, ?)')

            params = (action['category'], action['dt_1'], action['dt_2'])

    else:
        sql_str = ('update "action" '
                   '   set end_dt = ? '
                   ' where category = ? '
                   '   and end_dt is null')

        params = (action['dt_1'], action['category'])

    run_sql(sql_str, params)


def insert_journal_into_file(entry):
    pass


if __name__ == '__main__':
    # TODO: Convert to argparse and include location
    #       https://stackoverflow.com/a/33902937
    sys.argv.pop(0)
    entry = ' '.join(sys.argv)
    entry_type = get_entry_type(entry)

    if entry_type == 'transaction':
        print('tx')
        insert_tx_into_db(entry)

    if entry_type == 'todo':
        print('todo')
        insert_todo_into_file(entry)

    if entry_type == 'action':
        print('action')
        insert_action_into_db(entry)

    if entry_type == 'journal':
        print('journal')
        insert_journal_into_file(entry)

    if entry_type is None:
        print('No entry type')



