import json
from pathlib import Path
from collections import OrderedDict

__all__ = ('CurrencyInfo', 'currency_code',)

_not_defined = object()


class CurrencyInfo:
    """Storage of currency information.

    All currency information get from
    "Unicode Technical Reports"
    (C) http://www.unicode.org/reports/

    Once loaded currency information buffered
    in `_curr_info` class variable.

    Usage example:
        >>> curr_info = CurrencyInfo()
        >>> curr_info.codes()
        ['AED', 'AFN', 'ALL', ..., 'YER', 'ZAR', 'ZMW']
        >>> curr_info.symbols('UAH')
        ['UAH', 'грн.', '₴']
        >>> curr_info.decimals('BHD')
        3

    """
    _curr_info = None
    _currency_db_file = Path('data/currency.json')

    def __init__(self):
        cls = self.__class__
        if cls._curr_info is None:
            cls._curr_info = cls._load_currency_info()

    @classmethod
    def _load_currency_info(cls):
        """Load currency information from static json file.

        File structure:
            {
                <CODE>: {
                    decimals: <DECIMALS>,
                    symbols: [<SYMBOL>, <SYMBOL>, ...]
                }, ...
            }

        :return OrderDict[str, dict]:
        """
        try:
            with cls._currency_db_file.open() as cf:
                return OrderedDict(
                    sorted(json.load(cf).items(), key=lambda item: item[0]))

        except (FileNotFoundError,
                PermissionError,
                IsADirectoryError,
                UnicodeDecodeError) as err:
            raise RuntimeError(
                'Required "currency.json" file not found!') from err

        except json.JSONDecodeError as err:
            raise RuntimeError(
                'Error decode "currency.json" file!') from err

    def codes(self):
        """List of currency codes formatted according to the iso 4217.

        :return list[str]: currency codes
        """
        return list(self._curr_info.keys())

    def symbols(self, code):
        """List of currency symbols for specified currency code.

        Examples:
            UAH  =>  ['UAH', 'грн.', '₴']
            SYP  =>  ['LS', 'SYP', 'S£', '£', 'ل.س.\u200f']

        :param str code: currency code (iso 4217)
        :return list[str]: tuple of currency symbols as unicode strings
        :raise ValueError: missing currency code error
        """
        try:
            return self._curr_info[code]['symbols']
        except KeyError:
            raise ValueError(
                'Currency code "{code}" not found!'.format(code=code))

    def decimals(self, code):
        """Number of decimal digits in the fractional part of the price.

        Examples:
            JPY  =>  0
            USD  =>  2
            BHD  =>  3

        :param str code: currency code (iso 4217)
        :return int: number of decimal digits
        :raise ValueError: missing currency code error
        """
        try:
            return self._curr_info[code]['decimals']
        except KeyError:
            raise ValueError(
                'Currency code "{code}" not found!'.format(code=code))


def currency_code(raw_currency, default=_not_defined):
    """Get currency code from raw currency string.

    Convert raw currency string presented in any localization
    as a valid currency code string.

    If raw currency does not contain valid currency information or contains
    more than one currencies, then return default value.
    If default value not set, then raise ValueError.

    Examples:
        UAH   =>  UAH
        US$   =>  USD
        සිෆ්එ  =>  XOF
        $     =>  <default>  (symbols used for multiple currency codes)

    :param str raw_currency: string that contains currency information.
    :param default: value that will be returned if raw currency not valid.
    :return: currency code string.
    :raise ValueError: error if raw price not valid and default value not set.
    """
    possible_currencies = set()
    curr_info = CurrencyInfo()

    def _error_or_default(err_msg):
        if default == _not_defined:
            raise ValueError(err_msg)
        return default

    # check and clean
    if not isinstance(raw_currency, str):
        return _error_or_default(
            'Wrong raw currency type "{curr_type}" '
            '(expected type "str")'.format(curr_type=type(raw_currency)))

    currency = raw_currency.replace('\xa0', '').replace('\u200f', '').strip()
    if not currency:
        return _error_or_default(
            'Raw currency value "{curr}" does not contain '
            'currency code'.format(curr=raw_currency))

    # search currency code or currency symbol
    for code in curr_info.codes():
        if code in currency:
            possible_currencies.add(code)
            continue
        for symbol in curr_info.symbols(code):
            symbol = symbol[:-1] if symbol[-1] == '\u200f' else symbol
            if symbol in currency:
                possible_currencies.add(code)

    if len(possible_currencies) == 0:
        return _error_or_default('Currency code not found')

    if len(possible_currencies) > 1:
        return _error_or_default(
            'Found more than one currency '
            'code: {codes}'.format(codes=sorted(possible_currencies)))

    return possible_currencies.pop()
