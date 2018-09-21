import csv
import traceback
from datetime import datetime

import requests
from bs4 import BeautifulSoup

fieldnames = ['date', 'open', 'high', 'low', 'close', 'volume', 'marketcap']


def _str2num(s):
    num = 0
    if s == '-':
        num = 0
    elif ',' in s:
        num = s.replace(',', '')
    return num


def get_historical_data(website_slug):
    with open('data/{}.csv'.format(website_slug), 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        res = requests.get(
            'https://coinmarketcap.com/currencies/{}/historical-data/?start=20000428&end=20180921'.format(website_slug))
        soup = BeautifulSoup(res.text, 'lxml')
        rows = soup.select('#historical-data > div > div.table-responsive > table > tbody > tr')
        for row in rows:
            try:
                tds = row.select('td')

                d = {
                    'date': datetime.strptime(tds[0].get_text(), '%b %d, %Y').isoformat(),
                    'open': tds[1].get_text(),
                    'high': tds[2].get_text(),
                    'low': tds[3].get_text(),
                    'close': tds[4].get_text(),
                    'volume': _str2num(tds[5].get_text()),
                    'marketcap': _str2num(tds[6].get_text()),
                }
                writer.writerow(d)
            except:
                traceback.print_exc()


def crawl():
    res = requests.get('https://api.coinmarketcap.com/v2/listings/')
    if res.status_code == 200:
        res = res.json()
        for coin in res['data']:
            print('Get historical data ', coin['website_slug'])
            get_historical_data(coin['website_slug'])


if __name__ == '__main__':
    crawl()
