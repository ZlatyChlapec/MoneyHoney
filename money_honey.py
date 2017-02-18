import argparse
import json
from decimal import Decimal, InvalidOperation
from random import randint

from actual_currencies import CurrenciesChanger


class MoneyHoney(object):
    """
    You can't convert money if arguments weren't set before. Same with print_results(), it's hard to print them before
    money is converted.
    """
    def __init__(self):
        """
        Without instance of actual_currencies.CurrenciesChanger it's not possible to figure out which currencies are
        supported.
        """
        self.args = None
        self.currency_changer = CurrenciesChanger()
        self.converted_amounts = None

    def arguments_parser(self):
        args_parser = argparse.ArgumentParser()
        required_args = args_parser.add_argument_group("required arguments")
        required_args.add_argument("-a", "--amount", required=True, action=self.decimal_check(),
                                   help="Amount of money we want to exchange.")
        required_args.add_argument("-ic", "--input_currency", required=True,
                                   action=self.currency_check(self.currency_changer),
                                   help="Three chars code or currency symbol from which we are converting.")
        args_parser.add_argument("-oc", "--output_currency", required=False,
                                 action=self.currency_check(self.currency_changer),
                                 help="Three chars code or currency symbol to which we are converting.")
        args_parser.add_argument("-nj", "--no_json", required=False, action='store_true',
                                 help="Will change output format from json to custom one.")
        self.args = args_parser.parse_args()

    def currency_check(self, currency_changer):
        """
        Custom action for argument parser to restrict values of currency inputs.
        :param currency_changer: Instance of class actual_currencies.CurrenciesChanger.
        :return: Class which inherits from argparse.Action and takes care of restrictions.
        """
        class CurrencyCheck(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                if isinstance(values, str) and len(values) <= 3:
                    if not currency_changer.is_supported_currency(values.upper()):
                        parser.error("argument {0}/{1}: '{2}' is not supported currency."
                                     .format(self.option_strings[0], self.option_strings[1], values))
                else:
                    parser.error("argument {0}/{1}: has to be str no longer than 3 chars."
                                 .format(self.option_strings[0], self.option_strings[1]))

                setattr(namespace, self.dest, values)

        return CurrencyCheck

    def decimal_check(self):
        """
        Check for correct decimal. Could have been just class but to keep it consistent I went with func.
        :return: Decimal value.
        """
        class DecimalCheck(argparse.Action):
            def __call__(self, parser, namespace, values, option_string=None):
                try:
                    values = Decimal(values)
                except InvalidOperation:
                    parser.error("argument {0}/{1}: has to be Decimal."
                                 .format(self.option_strings[0], self.option_strings[1]))

                setattr(namespace, self.dest, values)

        return DecimalCheck

    def convert_money(self):
        """
        Prepare to inputs to get converted and convert.
        """
        self.handle_input_currency()
        self.handle_output_currency()
        self.currency_changer.set_exchange_params(self.args.amount, self.args.input_currency, self.args.output_currency)
        self.converted_amounts = self.currency_changer.get_changed_values()

    def handle_input_currency(self):
        # if currency is symbol
        if len(self.args.input_currency) != 3:
            # find all currency codes for that symbol
            currency_codes = self.convert_symbol(self.args.input_currency)
            # if there are more than one
            if len(currency_codes) > 1:
                # ask if he cares
                if input("Would you care to specify? y/n\n").lower() in ['y', 'yes']:
                    # if he does allow him to choose
                    print("You can choose from: {0}".format(currency_codes))
                    specified_cur_code = input("Enter specific currency code:\n").upper()
                    # if he chose correctly set that as new input_currency
                    if specified_cur_code in currency_codes:
                        self.args.input_currency = specified_cur_code
                    # if no give him hell
                    else:
                        print("You failed.")
                        self.handle_input_currency()
                # if he doesn't care me neither
                else:
                    self.args.input_currency = currency_codes[randint(0, (len(currency_codes) - 1))]
            # if symbol has just one currency don't bother user, just get rid of array
            else:
                self.args.input_currency = self.get_first_value(currency_codes)
        # if it's not symbol just make it upper so it looks nice in output
        else:
            self.args.input_currency = self.args.input_currency.upper()

    def handle_output_currency(self):
        # if currency is symbol get currencies to which to convert
        if len(self.args.output_currency) != 3:
            self.args.output_currency = self.convert_symbol(self.args.output_currency)
        # if it's char code just make sure it's upper and in array
        else:
            self.args.output_currency = [self.args.output_currency.upper()]

    def convert_symbol(self, symbol):
        """
        Converts symbol to currency char codes. Shouldn't be used before arguments_parser().
        :param symbol: Symbol we want to convert.
        :return: Array with currency codes for symbol.
        """
        return self.currency_changer.currency_signs[symbol]

    def print_results(self):
        if self.args.no_json:
            output_string_start = "\n" + str(self.args.amount) + " " + self.args.input_currency + " is"
            if len(self.converted_amounts) == 1:
                print(output_string_start + " " +
                      self.output_string_end(format(self.get_first_value(self.converted_amounts.values()), '.4f'),
                                             self.get_first_value(self.converted_amounts.keys())) +
                      ".")
            else:
                print(output_string_start)
                for currency, currency_amount in self.converted_amounts.items():
                    print("\t" + self.output_string_end(format(currency_amount, '>20.4f'), currency))
        else:
            output_json = {}

            converted_currencies = {}
            for currency, currency_amount in self.converted_amounts.items():
                converted_currencies[currency] = format(currency_amount, '.4f')

            output_json['input'] = {'amount': format(self.args.amount, '.4f'), 'currency': self.args.input_currency}
            output_json['output'] = converted_currencies
            print("\n" + json.dumps(output_json, indent=4))

    @staticmethod
    def get_first_value(my_list):
        return next(iter(my_list))

    @staticmethod
    def output_string_end(converted_amount, output_currency):
        return str(converted_amount) + " " + output_currency

if __name__ == "__main__":
    money_honey = MoneyHoney()
    money_honey.arguments_parser()
    money_honey.convert_money()
    money_honey.print_results()
