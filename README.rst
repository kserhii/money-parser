Money Parser
============


Description
-----------

Money Parser is a price and currency parsing utility.
It provides methods to extract price and currency information from the raw string.
There is a lot of different price and currency formats that present values with separators, spacing etc.
This library may help you to parse such data.


Limitation
----------

 - currency with 3 numbers after decimal point (e.g. KWD, see `ISO 4217`_)


Introduction
------------

Extracting price from raw ``str``::

   >>> from money_parser import price_str
   >>> price_str('₹1,50,087.99 \n')
   '150087.99'
   >>> price_dec('+12.007')
   Decimal('12007')

Installation
------------

::

   $ pip install money-parser

The library requires Python >= 3.4


Documentation
------------------

.. py:function:: price_str(raw_price, [default=<not_defined>], [dec_point='.'])

    Search and clean price value.

    Convert raw price string presented in any localization
    as a valid number string with an optional decimal point.

    If raw price does not contain valid price value or contains
    more than one price value, then return default value.
    If default value not set, then raise ValueError.

    :param str raw_price: string that contains price value.
    :param default: value that will be returned if raw price not valid.
    :param dec_point: symbol that separate integer and fractional parts.
    :return: cleaned price string or default value.
    :raise ValueError: error if raw price not valid and default value not set.

::

    >>> price_str('+12.007')
    '12007'
    >>> price_str('- 520,05')
    '-520.05'
    >>> price_str('1,000,777.5')
    '1000777.5'
    >>> price_str('1.777.000,99')
    '1777000.99'
    >>> price_str('99,77,11,000.1')
    '997711000.1'
    >>> price_str('USD 5,242 \t\n')
    '5242'
    >>> price_str('90 210.42', dec_point='|')
    '90210|42'
    >>> price_str(None, default='0')
    '0'
    >>> price_str(42.333, default=None) is None
    True
    >>> price_str(None)
    Traceback (most recent call last):
      ...
    ValueError: Wrong raw price type "<class 'NoneType'>" (expected type "str")
    >>> price_str('')
    Traceback (most recent call last):
      ...
    ValueError: Raw price value "" does not contain valid price digits
    >>> price_str('1..2')
    Traceback (most recent call last):
      ...
    ValueError: Raw price value "1..2" contains more than one price value


.. py:function:: price_dec(raw_price, [default=<not_defined>])

    Price decimal value from raw string.

    Extract price value from input raw string and
    present as Decimal number. Uses a price_str function for price parsing.

    If raw price does not contain valid price value or contains
    more than one price value, then return default value.
    If default value not set, then raise ValueError.

    :param str raw_price: string that contains price value.
    :param default: value that will be returned if raw price not valid.
    :return: Decimal price value.
    :raise ValueError: error if raw price not valid and default value not set.

::

    >>> price_dec('+12.007')
    Decimal('12007')
    >>> price_dec(': -10.99$')
    Decimal('-10.99')
    >>> price_dec('', default=Decimal('0'))
    Decimal('0')
    >>> price_dec('1..10', default=0)
    0
    >>> price_dec('410.5 - 555', default=None) is None
    True
    >>> price_dec(42.3)
    Traceback (most recent call last):
      ...
    ValueError: Wrong raw price type "<class 'float'>" (expected type "str")
    >>> price_dec('free')
    Traceback (most recent call last):
      ...
    ValueError: Raw price value "free" does not contain valid price digits
    >>> price_dec('2+2')
    Traceback (most recent call last):
      ...
    ValueError: Raw price value "2+2" contains more than one price value


Run Tests
------

Project has tests::

    $ make test

Also available tests with coverage::

    $ make cov


Source code
-----------

The project is hosted on GitHub_


Authors and License
-------------------

The ``money-parser`` package is written by Serhii Kostel.

It's *Apache 2* licensed and freely available.


.. _`ISO 4217`: https://en.wikipedia.org/wiki/ISO_4217
.. _GitHub: https://github.com/kserhii/money-parser
