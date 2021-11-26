import sqlite3
import sys
from datetime import datetime

# TODO: Convert to argparse and include location
#       https://stackoverflow.com/a/33902937
category = sys.argv[1]

try:
    dt_1 = sys.argv[2]
except IndexError:
    dt_1 = datetime.now()
    # print(now)
    # dt_1 = now.strftime('YYYY-MM-DD HH:MM:ss')
    print(dt_1)

try:
    dt_2 = sys.argv[3]
except IndexError:
    dt_2 = ''

# conn = sqlite3.connect('../../storage/shared/appdata/folderbox/data.db')
conn = sqlite3.connect('storage/shared/appdata/folderbox/data.db')

sql_str = ('select * '
           '  from action '
           ' where category = ? '
           '   and end_dt is null')

cursor = conn.execute(sql_str, (category,))

results = cursor.fetchall()

print(results)

if len(results) == 0:
    if not dt_2:
        print('no results')
        sql_str = ('insert '
                   '  into action '
                   '       (category, begin_dt) '
                   'values (?, ?)')

        args = (category, dt_1)

    else:
        sql_str = ('insert '
                   '  into action '
                   '       (category, begin_dt, end_dt) '
                   'values (?, ?, ?)')

        args = (category, dt_1, dt_2)

else:
    print('yes results')
    sql_str = ('update "action" '
               '   set end_dt = ? '
               ' where category = ? '
               '   and end_dt is null')

    args = (dt_1, category)

cursor = conn.execute(sql_str, args)

conn.commit()
conn.close()

