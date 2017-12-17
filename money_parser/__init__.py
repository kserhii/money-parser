import re
import decimal

__version__ = '0.0.1'

__all__ = ('price_str', 'price_dec',)


_CLEANED_PRICE_RE = re.compile('[+-]?(?:\d{1,3}[.,]?)+')
_FRACTIONAL_PRICE_RE = re.compile('^([\d.,]+)[.,](\d{1,2})$')

_not_defined = object()


def price_str(raw_price, default=_not_defined, dec_point='.'):
    """Search and clean price value.

    Convert raw price string presented in any localization
    as a valid number string with an optional decimal point.

    If raw price does not contain valid price value or contains
    more than one price value, then return default value.
    If default value not set, then raise ValueError.

    Examples:
        12.007          => 12007
        00012,33        => 12.33
        +1              => 1
        - 520.05        => -520.05
        1,000,777.5     => 1000777.5
        1.777.000,99    => 1777000.99
        1 234 567.89    => 1234567.89
        99.77.11.000,1  => 997711000.1
        NIO5,242        => 5242
        Not a MINUS-.45 => 45
          42  \t \n     => 42
                        => <default>
        1...2           => <default>

    :param str raw_price: string that contains price value.
    :param default: value that will be returned if raw price not valid.
    :param dec_point: symbol that separate integer and fractional parts.
    :return: cleaned price string.
    :raise ValueError: error if raw price not valid and default value not set.
    """
    def _error_or_default(err_msg):
        if default == _not_defined:
            raise ValueError(err_msg)
        return default

    # check and clean
    if not isinstance(raw_price, str):
        return _error_or_default(
            'Wrong raw price type "{price_type}" '
            '(expected type "str")'.format(price_type=type(raw_price)))

    price = re.sub('\s', '', raw_price)
    cleaned_price = _CLEANED_PRICE_RE.findall(price)

    if len(cleaned_price) == 0:
        return _error_or_default(
            'Raw price value "{price}" does not contain '
            'valid price digits'.format(price=raw_price))

    if len(cleaned_price) > 1:
        return _error_or_default(
            'Raw price value "{price}" contains '
            'more than one price value'.format(price=raw_price))

    price = cleaned_price[0]

    # clean truncated decimal (e.g. 99. -> 99)
    price = price.rstrip('.,')

    # get sign
    sign = ''
    if price[0] in {'-', '+'}:
        sign, price = price[0], price[1:]
        sign = '-' if sign == '-' else ''

    # extract fractional digits
    fractional = _FRACTIONAL_PRICE_RE.match(price)
    if fractional:
        integer, fraction = fractional.groups()
    else:
        integer, fraction = price, ''

    # leave only digits in the integer part of the price
    integer = re.sub('\D', '', integer)

    # remove leading zeros (e.g. 007 -> 7, but 0.1 -> 0.1)
    integer = integer.lstrip('0')
    if integer == '':
        integer = '0'

    # construct price
    price = sign + integer
    if fraction:
        price = ''.join((price, dec_point, fraction))

    return price


def price_dec(raw_price, default=_not_defined):
    """Price decimal value from raw string.

    Extract price value from input raw string and
    present as Decimal number.

    If raw price does not contain valid price value or contains
    more than one price value, then return default value.
    If default value not set, then raise ValueError.

    :param str raw_price: string that contains price value.
    :param default: value that will be returned if raw price not valid.
    :return: Decimal price value.
    :raise ValueError: error if raw price not valid and default value not set.
    """
    try:
        price = price_str(raw_price)
        return decimal.Decimal(price)

    except ValueError as err:
        if default == _not_defined:
            raise err

    return default
