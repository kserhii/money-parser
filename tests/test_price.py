from decimal import Decimal

import pytest

from money_parser import price_str, price_dec


price_str_test_cases = [
    # Integer
    ('0', '0'),
    ('42', '42'),
    ('1234', '1234'),
    ('1 234', '1234'),
    ('1 234 567', '1234567'),
    ('12.007', '12007'),
    ('12,007', '12007'),
    ('1.234.567', '1234567'),
    ('1,234,567', '1234567'),
    ('1,034.550', '1034550'),

    # Start with zero
    ('042', '42'),
    ('0.01', '0.01'),
    ('00.1', '0.1'),
    ('0 234', '234'),
    ('000 567', '567'),
    ('012.33', '12.33'),
    ('00012,33', '12.33'),

    # Signed
    ('+1', '1'),
    ('-2.99', '-2.99'),
    ('-520', '-520'),
    ('+520', '520'),
    ('- 520.05', '-520.05'),
    ('+ 520.05', '520.05'),

    # Truncated decimal
    ('99.', '99'),
    ('99,', '99'),
    ('1,099.', '1099'),
    ('1.099,', '1099'),

    # One decimal digit
    ('42.0',    '42.0'),
    ('42,0',    '42.0'),
    ('10 380,5', '10380.5'),
    ('10 380.5', '10380.5'),
    ('10.380,5', '10380.5'),
    ('10,380.5', '10380.5'),
    ('1 000 777.5', '1000777.5'),
    ('1 000 777,5', '1000777.5'),
    ('1.000.777,5', '1000777.5'),
    ('1,000,777.5', '1000777.5'),

    # Two decimal digits
    ('10.99', '10.99'),
    ('10,99', '10.99'),
    ('1234567.89', '1234567.89'),
    ('1234567,89', '1234567.89'),
    ('12 345,09', '12345.09'),
    ('12 345.09', '12345.09'),
    ('12.345,09', '12345.09'),
    ('12,345.09', '12345.09'),
    ('1 234 567.89', '1234567.89'),
    ('1 234 567,89', '1234567.89'),
    ('1.234.567,89', '1234567.89'),
    ('1,234,567.89', '1234567.89'),

    # Indian numbering system
    ('5,00,111', '500111'),
    ('5.00.111', '500111'),
    ('12,13,14,007', '121314007'),
    ('12.13.14.007', '121314007'),
    ('7,01,02,03,999', '7010203999'),
    ('7.01.02.03.999', '7010203999'),

    ('1,00,222.1', '100222.1'),
    ('1.00.222,1', '100222.1'),
    ('99,77,11,000.1', '997711000.1'),
    ('99.77.11.000,1', '997711000.1'),

    ('5,00,111.99', '500111.99'),
    ('5.00.111,99', '500111.99'),
    ('12,13,14,007.99', '121314007.99'),
    ('12.13.14.007,99', '121314007.99'),

    # Price with rubbish
    ('  42  \t \n', '42'),
    ('|620|\" ]', '620'),
    ('|620.0|\" ]', '620.0'),
    ('|620,99\'|\" ]', '620.99'),
    ('[ * |"620.99"| * ]', '620.99'),
    ('\u200e \\500 "\n \n', '500'),
    ('"855.000|', '855000'),
    ('NIO5,242', '5242'),
    ('NIO5.242', '5242'),
    ('NIO5,242.7', '5242.7'),
    ('CFA10,615', '10615'),
    ('$10.99', '10.99'),
    ('USD 10,99', '10.99'),
    ('10.99$', '10.99'),
    ('10,99USD', '10.99'),
    ('99 ₣', '99'),
    ('Price:-9.99$', '-9.99'),
    ('Price:- 9,99 ₪', '-9.99'),
    ('Start with DOT.45', '45'),
    ('Start with COMMA,45', '45'),
    ('Not a MINUS-.45', '45'),
    ('Not a PLUS+,45', '45'),
]

wrong_price_str_test_cases = [
    # Wrong type
    None, object(), b'22', 23, 24.3, Decimal('25'),
    # No a price
    '', '1...2', '+', '-', 'USD', '-NuN', '+inf',
    # Two prices
    '90 BH 210', '90-60', '451 °F = 233 °C', '50.431782|30.516382'
]


@pytest.mark.parametrize("raw_price,price", price_str_test_cases)
def test_price_str_value(raw_price, price):
    assert price == price_str(raw_price)


@pytest.mark.parametrize("wrong_raw_price", wrong_price_str_test_cases)
def test_price_str_default(wrong_raw_price):
    default = object()
    assert default == price_str(wrong_raw_price, default=default)


@pytest.mark.parametrize("wrong_raw_price", wrong_price_str_test_cases)
def test_price_str_error(wrong_raw_price):
    with pytest.raises(ValueError):
        price_str(wrong_raw_price)


def test_price_str_dec_point():
    assert '9.99' == price_str('9,99')
    assert '9|99' == price_str('9,99', dec_point='|')


def test_price_dec_value():
    assert Decimal('1') == price_dec('+1')
    assert Decimal('-10.99') == price_dec(': -10.99$')


def test_price_dec_default():
    assert Decimal('0') == price_dec('', default=Decimal('0'))
    assert 0 == price_dec('1..10', default=0)
    assert price_dec('410.5 - 555', default=None) is None


def test_price_dec_error():
    with pytest.raises(ValueError):
        price_dec('')
    with pytest.raises(ValueError):
        price_dec('7 | 128')
