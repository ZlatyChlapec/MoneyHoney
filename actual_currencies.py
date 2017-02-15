import sys

from decimal import Decimal

from currencies_fetcher import CurrenciesRates


class CurrenciesChanger:
    def __init__(self):
        self.currency_rates = CurrenciesRates.fetch_currencies()
        # I could probably try and get them from http://www.xe.com/symbols.php but since I want to get them just once
        # and not every time program runs, here we go.
        self.currency_signs = {'€': ['EUR'], '$': ['AUD', 'CAD', 'MXN', 'NZD', 'SGD', 'USD'], 'лв': ['BGN'],
                               'R$': ['BRL'], '¥': ['CNY', 'JPY'], 'Kč': ['CZK'], 'kr': ['DKK', 'NOK', 'SEK'],
                               '£': ['GBP'], 'HK$': ['HKD'], 'kn': ['HRK'], 'Ft': ['HUF'], 'Rp': ['IDR'], '₪': ['ILS'],
                               '₹': ['INR'], '₩': ['KRW'], 'RM': ['MYR'], '₱': ['PHP'], 'zł': ['PLN'], 'lei': ['RON'],
                               '₽': ['RUB'], '฿': ['THB'], '₺': ['TRY'], 'R': ['ZAR']}

        self.amount = None
        self.currency_from = None
        self.currencies_to = None

    def set_exchange_params(self, amount, currency_from, currencies_to):
        self.amount = amount
        self.currency_from = currency_from
        self.currencies_to = currencies_to

    def change_currency_to_eur(self):
        return self.amount / Decimal(self.currency_rates['rates'][self.currency_from])

    def change_to_desired_currency(self, amount_eur, currency):
        return amount_eur * Decimal(self.currency_rates['rates'][currency])

    def get_changed_values(self):
        changed_values = {}
        currency_eur = self.amount

        if self.currency_from != 'EUR':
            currency_eur = self.change_currency_to_eur()

        if self.currencies_to is None:
            self.currencies_to = list(self.currency_rates['rates'].keys()) + ['EUR']
            self.currencies_to.remove(self.currency_from)

        # Common intellij it can't be None at this point
        for currency in self.currencies_to:
            if currency == 'EUR':
                changed_values['EUR'] = currency_eur
            else:
                changed_values[currency] = self.change_to_desired_currency(currency_eur, currency)

        return changed_values

    def is_supported_currency(self, currency):
        if self.currency_rates['base'] == 'EUR':
            if currency in (list(self.currency_rates['rates'].keys()) + ['EUR'])\
                    or currency in list(self.currency_signs.keys()):
                return True
            else:
                return False
        else:
            print("Exchange rates provider changed API and application needs to be updated accordingly.")
            sys.exit(1)
