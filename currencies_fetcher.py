import json
import urllib.request
from urllib.error import URLError, HTTPError


# TODO: actualise latest_rates.json with new data on each connect
# TODO: if date of actual currencies is same as today don't fetch them
class CurrenciesRates:

    @staticmethod
    def fetch_currencies():
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
        return CurrenciesRates.fetch_from_fixer()

    @staticmethod
    def fetch_from_fixer():
        try:
            print("Fetching currency rates from https://api.fixer.io/latest.")
            currencies = urllib.request.urlopen("https://api.fixer.io/latest")
            print("Fetched successfully.")
            return json.loads(currencies.read().decode('utf-8'))
        # TODO: merge both exception to one and make sane output
        except HTTPError as e:
            print(e)
        except URLError as e:
            print("Couldn't load fresh currency rates from internet.\nFalling back to latest offline data.")
            return CurrenciesRates.fetch_from_file()

    @staticmethod
    def fetch_from_file():
        with open('latest_rates.json') as latest_rates:
            return json.loads(latest_rates.read())
