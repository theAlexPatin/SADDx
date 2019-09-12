from dotenv import load_dotenv
import os
import requests
import datetime
import json

load_dotenv()

# an app token registered with the Accuweather API
WEATHERSTACK_KEY = os.getenv('WEATHERSTACK_KEY')

CITY = 'Boston'

START_DATE = datetime.datetime.now() - datetime.timedelta(days=365)

def _get_date_format(date):
    year = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = '0'+month
    day = str(date.day)
    if len(day) == 1:
        day = '0'+day
    return '{}-{}-{}'.format(year, month, day)

def main():
    temps = {}
    d = START_DATE
    for i in range(0,366):
        date = _get_date_format(d)
        url = 'http://api.weatherstack.com/historical?access_key={}&units=f&query={}&hourly=0&historical_date={}'.format(WEATHERSTACK_KEY, CITY, date)
        data = requests.get(url).json()
        temps[date] = data['historical'][date]['avgtemp']
        d = d + datetime.timedelta(days=1)
    with open('temperatures.json', 'w') as f:
        json.dump(temps, f, indent=4)

if __name__ == '__main__':
    main()
