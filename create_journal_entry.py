import shutil
from datetime import datetime

journal_org_file_path = '/data/data/com.termux/files/home/storage/shared/notes/notes/journal.org'
current_date_str = datetime.now().strftime('%Y-%m-%d')
current_time_str = datetime.now().strftime('%H-%M')

entry_file_path = f'/data/data/com.termux/files/home/storage/shared/notes/entries/{current_date_str}-bryce-eryn-caine-journal-{current_time_str}.txt'

# Copy journal.org to new entry file
shutil.copyfile(journal_org_file_path, entry_file_path)

# Clear contents of journal.org
open(journal_org_file_path, 'w').close()

print('hola')

