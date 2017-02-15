import json
import urllib.request
from datetime import datetime
from time import mktime, strptime
from urllib.error import URLError


class CurrencyRates:
    """
    For production use I would recommend adding more sources of currency rates.
    """
    def __init__(self):
        self.currency_rates = CurrencyRates._fetch_from_file()
        self.data_date = datetime.fromtimestamp(mktime(strptime(self.currency_rates['date'], "%Y-%m-%d"))).date()
        current_date = datetime.now().date()

        if self.data_date != current_date:
            self._fetch_from_fixer()

    def get_rates(self):
        """
        JSON format:
        {
          "base": "EUR",
          "date": "2017-02-08",
          "rates": {
            "AUD": 1.396,
            "BGN": 1.9558
            ...
          }
        }
        :return: JSON with currencies rates.
        """
        return self.currency_rates

    def _fetch_from_fixer(self):
        """
        Downloads currencies from https://api.fixer.io/latest. Sets them to self.currency_rates and saves them to file
        for offline use.
        """
        try:
            print("Fetching currency rates from https://api.fixer.io/latest.")
            currencies = urllib.request.urlopen("https://api.fixer.io/latest")
        except URLError:
            print("Couldn't load fresh currency rates from internet.\nFalling back to latest offline data ", end='')
            print("from " + self.data_date.strftime('%d.%m.%Y') + ".")
        else:
            print("Fetched successfully.")
            json_string = currencies.read().decode('utf-8')
            self.currency_rates = json.loads(json_string)
            self._save_to_file(json_string)

    @staticmethod
    def _fetch_from_file():
        with open('latest_rates.json', encoding='utf-8') as latest_rates:
            return json.loads(latest_rates.read())

    @staticmethod
    def _save_to_file(string):
        with open('latest_rates.json', 'w', encoding='utf-8') as latest_rates:
            latest_rates.write(string)
