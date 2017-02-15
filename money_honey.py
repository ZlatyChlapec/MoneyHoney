import json
import sys
import getopt
from decimal import Decimal, InvalidOperation
from random import randint

from actual_currencies import CurrenciesChanger


class MoneyHoney:
    """
    I wasn't sure if it's allowed to use external libraries so I didn't use any.
    Estimated time of coding 4MD.
    """
    def __init__(self):
        pass

    def arguments_handler(self):
        """
        Handles the arguments and flow of the program.
        """
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "amount=", "input_currency=", "output_currency=",
                                                           "no_json"])
        except getopt.GetoptError as err:
            print(err, "\n")
            self.usage()
            sys.exit(2)

        amount = None
        input_currency = None
        output_currency = None
        no_json = False
        currency_changer = CurrenciesChanger()

        for arg, value in opts:
            if arg in ("-h", "--help"):
                self.usage()
                sys.exit()
            elif arg == "--amount":
                try:
                    amount = Decimal(value)
                except InvalidOperation:
                    print("Couldn't parse amount. Make sure you are using valid number.")
                    sys.exit(1)
            elif arg == "--input_currency":
                input_currency = self.check_currency(currency_changer, arg, value)
            elif arg == "--output_currency":
                output_currency = self.check_currency(currency_changer, arg, value)
            elif arg == "--no_json":
                no_json = True

        output_string_start = "\n" + str(amount) + " " + input_currency + " is"
        if amount is None or input_currency is None:
            print("You need to specify required parameters.\n")
            self.usage()
            sys.exit(2)
        else:
            currency_changer.set_exchange_params(amount, input_currency, output_currency)
            converted_amounts = currency_changer.get_changed_values()

            if no_json:
                if len(converted_amounts) == 1:
                    print(output_string_start + " " + self.output_string_end(format(self.get_first_value(
                        converted_amounts.values()), '.4f'), self.get_first_value(converted_amounts.keys())) + ".")
                else:
                    print(output_string_start)
                    for currency, currency_amount in converted_amounts.items():
                        print("\t" + self.output_string_end(format(currency_amount, '>20.4f'), currency))
            else:
                output_json = {}

                converted_currencies = {}
                for currency, currency_amount in converted_amounts.items():
                    converted_currencies[currency] = format(currency_amount, '.4f')

                output_json['input'] = {'amount': format(amount, '.4f'), 'currency': input_currency}
                output_json['output'] = converted_currencies
                print("\n" + json.dumps(output_json, indent=4))

    @staticmethod
    def get_first_value(my_list):
        return next(iter(my_list))

    @staticmethod
    def output_string_end(converted_amount, output_currency):
        return str(converted_amount) + " " + output_currency

    def check_currency(self, currency_changer, name, currency, symbol_currencies=None):
        """
        Checks if currency is valid and supported.
        :param currency_changer: Instance of CurrenciesChanger.
        :param name: Name of the input.
        :param currency: Currency symbol or letter code.
        :param symbol_currencies: Array of currency codes for specific symbol.
        :return: Check function convert_symbol for returns.
        """
        if symbol_currencies is not None and currency.upper() in symbol_currencies:
            return currency
        elif symbol_currencies is None and currency_changer.is_supported_currency(currency.upper()):
            return self.convert_symbol(currency_changer, name, currency)
        else:
            print("Incorrect " + name[2:] + ". Either it isn't supported or you messed up on your part.")
            sys.exit(1)

    def convert_symbol(self, currency_changer, input_name, symbol):
        """
        Converts all symbols to currency code and puts "--output_currency" into array.
        :param currency_changer: Instance of class actual_currencies.CurrenciesChanger.
        :param input_name: Name of the input. [--input_currency, --output_currency]
        :param symbol: Symbol or currency code.
        :return: Value if input_name equals "--input_currency", array otherwise.
        """
        if symbol in list(currency_changer.currency_signs.keys()):
            currency_codes = currency_changer.currency_signs[symbol]
            if input_name == "--input_currency" and len(currency_codes) > 1:
                if input("Would you care to specify? y/n\n").lower() in ['y', 'yes']:

                    print("You can choose from: [", end='')
                    for i in range(len(currency_codes)):
                        if i == len(currency_codes) - 1:
                            print(currency_codes[i] + "]")
                        else:
                            print(currency_codes[i] + "; ", end='')

                    return self.check_currency(currency_changer, input_name, input("Enter specific currency code:\n"),
                                               currency_codes).upper()
                else:
                    num_options = len(currency_codes)
                    return currency_codes[randint(0, (num_options - 1))]
            else:
                return currency_codes[0] if input_name == "--input_currency"\
                                            and len(currency_codes) == 1 else currency_codes
        else:
            # it's not symbol
            return symbol.upper() if input_name == "--input_currency" else [symbol.upper()]

    @staticmethod
    def usage():
        print("--amount\n\tRequired. Can contain only number.\n"
              "--input_currency\n\tRequired. Can contain only three chars or currency symbol.\n"
              "--output_currency\n\tOptional. Can contain only three chars or currency symbol.\n"
              "--no_json\n\tOptional. Will change output format from json to custom one.")


if __name__ == "__main__":
    MoneyHoney().arguments_handler()
