#!../venv/bin/python
import json
import os
import requests
import shutil
from datetime import datetime
from geopy.geocoders import Nominatim

journal_org_file_path = '/data/data/com.termux/files/home/storage/shared/notes/notes/journal.org'
current_date_str = datetime.now().strftime('%Y-%m-%d')
current_time_str = datetime.now().strftime('%H-%M-%f')

entry_file_path = f'/data/data/com.termux/files/home/storage/shared/notes/entries/{current_date_str}-bryce-eryn-caine-journal-{current_time_str}.txt'

# Copy journal.org to new entry file
shutil.copyfile(journal_org_file_path, entry_file_path)

# Clear contents of journal.org
# open(journal_org_file_path, 'w').close()

# Get front matter
author = 'author: Bryce Caine'
entry_date = f'date: {current_date_str}'
tags = 'tags: journal'
location_dict = json.loads(os.popen('termux-location').read())
latitude = location_dict['latitude']
longitude = location_dict['longitude']
altitude_ft = round(location_dict['altitude'] * 3.28084)
altitude = f'altitude: {altitude_ft}'
app = Nominatim(user_agent='journal')
coordinates = f'{latitude}, {longitude}'
location_raw = app.reverse(coordinates, language='en').raw
house_number = location_raw['address']['house_number']
road = location_raw['address']['road']
town = location_raw['address']['town']
state = location_raw['address']['state']
location = f'location: {house_number} {road}, {town}, {state}'
# location = location_raw['display_name']
# location = f'latitude: {latitude}\nlongitude: {longitude}\naltitude: {altitude}'
weather_response = requests.get('http://wttr.in/?format=%C+%t+%h+humidity+%w+wind+%p+precip')
weather = f'weather: {weather_response.text}'
front_matter = f'---\n{author}\n{entry_date}\n{tags}\n{location}\n{altitude}\n{weather}\n---\n'
with open(entry_file_path, 'r') as journal_org_file: journal_org_data = journal_org_file.read()
with open(entry_file_path, 'w') as entry_file: entry_file.write(front_matter + journal_org_data)

# termux-open --choose $entry_file_path

print('hola')

