import sqlite3


from datetime import datetime
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
    tx_date = None

    for item in items:
        try:
            tx_date = parse(item)
            break
        except ParserError:
            tx_date = datetime.now()

    return tx_date
        

def parse_transaction(entry):
    print(f'----- {entry}')
    parts = entry.split(' ')
    amount = parts.pop(0)
    details = ' '.join(parts)
    print(amount)

    try:
        tx_date = parse(details)
    except ParserError:
        parts = details.split(' ')
        tx_date = get_date_from_list(parts)

        if tx_date is None:
            tx_date = datetime.now()

    print(tx_date)

for entry in entries:
    tx = parse_transaction(entry)
    


conn = sqlite3.connect('budgetous.db')
c = conn.cursor()

c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
conn.commit()
conn.close()
