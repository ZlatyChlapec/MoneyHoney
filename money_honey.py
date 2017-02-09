import sys
import getopt
from decimal import Decimal, InvalidOperation

from actual_currencies import CurrenciesChanger


def main():
    """
     I wasn't sure if it's allowed to use external libraries so I didn't use any.
    """
    # Handles input of application.
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "amount=", "input_currency=", "output_currency="])
    except getopt.GetoptError as err:
        print(err, "\n")
        usage()
        sys.exit(2)

    amount = None
    input_currency = None
    output_currency = None

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "--amount":
            try:
                amount = Decimal(a)
            except InvalidOperation:
                print("Couldn't parse amount. Make sure you are using valid number.")
                sys.exit(1)
        elif o == "--input_currency":
            input_currency = check_currency(o, a)
        elif o == "--output_currency":
            output_currency = check_currency(o, a)

    # Handles output of application
    output_string_start = amount + " " + input_currency + " is"
    if amount is None or input_currency is None:
        print("You need to specify required parameters.\n")
        usage()
        sys.exit(2)
    else:
        converted_amounts = CurrenciesChanger(amount, input_currency, output_currency).get_changed_values()

        if len(converted_amounts) == 1:
            print(output_string_start + " " + output_string_end(str(get_first_value(converted_amounts.values())),
                                                                get_first_value(converted_amounts.keys())) + ".")
        else:
            print(output_string_start)
            for cur, ca in converted_amounts.items():
                print("\t" + output_string_end(ca, cur))


def get_first_value(my_list):
    return next(iter(my_list))


def output_string_end(converted_amount, output_currency):
    return str(converted_amount) + " " + output_currency


def check_currency(name, currency):
    if CurrenciesChanger.is_valid_currency(currency):
        return currency
    else:
        print("Couldn't parse " + name[2:] + ". Either it isn't supported or you messed up on your part.")
        sys.exit(1)


def usage():
    print("--amount\n\tRequired. Can contain only number.\n"
          "--input_currency\n\tRequired. Can contain only three chars or currency symbol.\n"
          "--output_currency\n\tOptional. Can contain only three chars or currency symbol.")


if __name__ == "__main__":
    main()
