import sys

from decimal import Decimal

from currencies_fetcher import CurrencyRates


class CurrenciesChanger(object):
    """
    Exchange currencies based on currency rates. You need to use set_exchange_params before using any other functions
    from this class.
    """
    def __init__(self):
        self.currency_rates = CurrencyRates().get_rates()
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
        """
        Set's variables so this class can work.
        :param amount: Amount of money we want to change.
        :param currency_from: Currency in which money are.
        :param currencies_to: Array with Currencies to which we want to change.
        """
        self.amount = amount
        self.currency_from = currency_from
        self.currencies_to = currencies_to

    def change_currency_to_eur(self):
        return self.amount / Decimal(self.currency_rates['rates'][self.currency_from])

    def change_to_desired_currency(self, amount_eur, currency):
        return amount_eur * Decimal(self.currency_rates['rates'][currency])

    def get_changed_values(self):
        """
        Based on setup of class changes currency to desired currencies.
        :return: Changed currencies in dictionary e.g. {'EUR': value}
        """
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
        """
        Checks if currency is supported by current setup.
        :param currency: Currency we want to check.
        :return: True if currency is supported, False if it's not.
        """
        if self.currency_rates['base'] == 'EUR':
            if currency in (list(self.currency_rates['rates'].keys()) + ['EUR'])\
                    or currency in list(self.currency_signs.keys()):
                return True
            else:
                return False
        else:
            print("Exchange rates provider changed API and application needs to be updated accordingly.")
            sys.exit(1)
