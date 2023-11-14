import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, date
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://www.usatoday.com/celebrity-deaths/"

def parse_date(date_array: list) -> str:
    """Parse date from array and format it as YYYY-MM-DD."""
    if date_array:
        return datetime.strptime(date_array[0], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')
    return None

data = []

current_year = date.today().year

for year in range(2018, current_year + 1):
    url = f'{BASE_URL}{year}'
    try:
        with requests.get(url) as response:
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                script_tag = soup.find('script', id='__NEXT_DATA__')
                if script_tag:
                    json_data = script_tag.string.strip()
                    json_dict = json.loads(json_data)

                    celebrities = json_dict['props']['pageProps']['assets']['assets']
                    for asset in celebrities:
                        primary_tag = next((tag for tag in asset['tags'] if tag.get('isPrimary')), None)
                        if primary_tag:
                            name = primary_tag['tag']['name']
                            birthdate = parse_date(primary_tag['tag']['attributes']['birthdate'])
                            deathdate = parse_date(primary_tag['tag']['attributes']['deathdate'])
                            if birthdate and deathdate:
                                data.append({'name': name, 'birthdate': birthdate, 'deathdate': deathdate})
                else:
                    logging.warning(f'No data found for the year {year}')
            else:
                logging.error(f'Failed to retrieve data for the year {year}')
    except Exception as e:
        logging.error(f'Error occurred for year {year}: {e}')

celebrities_df = pd.DataFrame(data)

celebrities_df['deathdate'] = pd.to_datetime(celebrities_df['deathdate'])

# Exclude Mary Tyler Moore who is on the 2019 page but died in 2017.
# This will also excude future edge cases like this to ensure the results are all 2018+.
celebrities_df = celebrities_df[celebrities_df['deathdate'].dt.year >= 2018]

# The USA Today site lists his death as Feb 2, 2023, but it's actually Feb 26
celebrities_df.loc[celebrities_df['name'] == 'Terry Holland', 'deathdate'] = '2023-02-26'

# And finally remove Julian Sands, who died in January 2023 but whose body wasn't discovered until June,
# presenting challenges for models like GPT-4 Turbo which has a knowledge cutoff of April 2023.
celebrities_df = celebrities_df[celebrities_df['name'] != 'Julian Sands']

celebrities_df.sort_values(by=['deathdate'], inplace=True)

celebrities_df.to_csv('celebrity_deaths.csv', index=False)

print(celebrities_df)
