import json
import os
from datetime import date

import requests
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
from geopy.geocoders import Nominatim

ENTRY_DIR = os.environ['ENTRY_DIR']
JOURNAL_MEMOS_DIR = os.environ['JOURNAL_MEMOS_DIR']


def get_front_matter(memo_date):
    # Author
    author = 'author: Bryce Caine'

    # Date
    memo_date_str = (memo_date).strftime('%Y-%m-%d')
    entry_date = f'date: {memo_date_str}'

    # Tags
    tags = 'tags: journal'
    
    # Location
    try:
        location_dict = json.loads(os.popen('termux-location').read())
        latitude = location_dict['latitude']
        longitude = location_dict['longitude']
        altitude_ft = round(location_dict['altitude'] * 3.28084)
        altitude = f'altitude: {altitude_ft}'
        geolocator = Nominatim(user_agent='journal')
        coordinates = f'{latitude}, {longitude}'
        location_raw = geolocator.reverse(coordinates, language='en').raw
        house_number = location_raw['address']['house_number']
        road = location_raw['address']['road']
        try:
            town = location_raw['address']['town']
        except KeyError:
            town = location_raw['address']['suburb']
        state = location_raw['address']['state']
        location = f'location: {house_number} {road}, {town}, {state}'
        # location = location_raw['display_name']
        # location = f'latitude: {latitude}\nlongitude: {longitude}\naltitude: {altitude}'

    except json.decoder.JSONDecodeError:
        location = f'location: Unknown'
        altitude = f'altitude: Unknown'

    # Weather
    weather_response = requests.get('http://wttr.in/?format=%C+%t+%h+humidity+%w+wind+%p+precip')
    weather = f'weather: {weather_response.text}'

    front_matter = f'---\n{author}\n{entry_date}\n{tags}\n{location}\n{altitude}\n{weather}\n---\n'

    return front_matter


def insert_into_file(entry):
    # Get journal_tally_file
    journal_tally_filename = f'{ENTRY_DIR}/journal_tally.txt'

    with open(journal_tally_filename, 'r+') as journal_tally_file: 
        today = date.today()
        
        # Get date from journal_tally_file
        journal_tally_data = journal_tally_file.read().splitlines(True)
        
        try:
            journal_tally_date = parse(journal_tally_data[0])
            journal_tally_date = date(journal_tally_date.year, journal_tally_date.month, journal_tally_date.day)

        except (IndexError, ParserError):
            journal_tally_date = date(today.year, today.month, today.day)
            # Insert journal_tally_date into file
            journal_tally_file.truncate(0)
            journal_tally_file.write(f'{journal_tally_date}\n')
            journal_tally_file.writelines(journal_tally_data)

        if journal_tally_date != today:
            # Copy journal_tally_file to dated_file
            journal_tally_date_str = (journal_tally_date).strftime('%Y-%m-%d')

            dated_journal_filename = f'{JOURNAL_MEMOS_DIR }/{journal_tally_date_str}-bryce-eryn-caine-journal.txt'

            # Add front_matter to dated_file
            front_matter = get_front_matter(journal_tally_date)

            with open(dated_journal_filename, 'w') as dated_journal_filename:
                dated_journal_filename.write(front_matter)
                dated_journal_filename.writelines(journal_tally_data[1:])

            # Clear contents of journal_tally_file
            journal_tally_file.truncate(0)

            # Add date to journal_tally_file
            journal_tally_file.write(f'{today}\n')

        # Add entry to journal_tally_file
        journal_tally_file.write(f'{entry}\n')
