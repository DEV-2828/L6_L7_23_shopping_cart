"""Statement coverage tests for the assigned shopping cart module.

Run from this directory:

"""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    "category, price, qty, expected",
    [
        ("food", 100, 2, 210),
        ("electronics", 100, 1, 118),
        ("clothing", 100, 10, 1008),
        ("food", 100, 9, 945),
        ("food", 100, 10, 945),
        ("food", 0, 1, 0),
        ("electronics", 99, 1, 116),
        ("food", 11, 11, 114),
    ],
)
def test_item_totals(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


def test_unknown_category():
    with pytest.raises(ValueError, match="^unknown category$"):
        item_total("books", 100, 1)


def test_negative_price():
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", -1, 1)


@pytest.mark.parametrize("qty", [0, -1])
def test_nonpositive_quantity(qty):
    with pytest.raises(ValueError, match="^invalid price or quantity$"):
        item_total("food", 100, qty)


@pytest.mark.parametrize(
    "cart_value, is_prime, coupon, expected",
    [
        (500, False, None, 0),
        (2500, False, None, 200),
        (5000, True, "FLAT10", 1100),
        (1999, False, None, 0),
        (2000, False, None, 200),
        (4999, False, None, 200),
        (5000, False, None, 500),
        (999, False, "FLAT10", 0),
        (1000, False, "FLAT10", 100),
        (1009, False, "FLAT10", 100),
    ],
)
def test_cart_discounts(cart_value, is_prime, coupon, expected):
    assert cart_discount(cart_value, is_prime, coupon) == expected


@pytest.mark.parametrize(
    "cart_value, is_prime, is_express, expected",
    [
        (100, False, False, 40),
        (500, False, False, 0),
        (100, True, True, 50),
        (100, False, True, 140),
        (499, False, False, 40),
        (499, False, True, 140),
        (500, False, True, 100),
        (0, True, False, 0),
    ],
)
def test_shipping_fees(cart_value, is_prime, is_express, expected):
    assert shipping_fee(cart_value, is_prime, is_express) == expected
