"""Branch coverage tests for the assigned shopping cart module.

Run from this directory:
    python -m coverage run --branch --source=shopping_cart -m pytest BranchCoverageTest_23_shopping_cart.py
    python -m coverage report -m

Explicit filenames are required because these submission filenames do not
match pytest's default test discovery pattern.
"""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    "category, price, qty, message",
    [
        pytest.param("books", 100, 1, "unknown category", id="unknown-category"),
        pytest.param("food", -1, 1, "invalid price or quantity", id="negative-price"),
        pytest.param("food", 100, 0, "invalid price or quantity", id="zero-quantity"),
        pytest.param("food", 100, -1, "invalid price or quantity", id="negative-quantity"),
    ],
)
def test_item_rejection_branches(category, price, qty, message):
    with pytest.raises(ValueError, match=f"^{message}$"):
        item_total(category, price, qty)


@pytest.mark.parametrize(
    "qty, expected",
    [
        pytest.param(9, 945, id="without-bulk-discount"),
        pytest.param(10, 945, id="with-bulk-discount"),
    ],
)
def test_bulk_discount_branches(qty, expected):
    assert item_total("food", 100, qty) == expected


@pytest.mark.parametrize(
    "cart_value, is_prime, coupon, expected",
    [
        pytest.param(1999, False, None, 0, id="lower-discount-tier"),
        pytest.param(2000, False, None, 200, id="middle-discount-tier"),
        pytest.param(5000, False, None, 500, id="upper-discount-tier"),
        pytest.param(4999, False, None, 200, id="just-below-upper-tier"),
        pytest.param(0, True, None, 100, id="prime-discount"),
        pytest.param(999, False, "FLAT10", 0, id="coupon-below-minimum"),
        pytest.param(1000, False, "FLAT10", 100, id="coupon-at-minimum"),
        pytest.param(1000, False, "OTHER", 0, id="wrong-coupon-above-minimum"),
        pytest.param(1000, False, "flat10", 0, id="coupon-is-case-sensitive"),
        pytest.param(2000, True, "FLAT10", 500, id="middle-tier-prime-and-coupon"),
        pytest.param(5000, True, "FLAT10", 1100, id="upper-tier-prime-and-coupon"),
    ],
)
def test_cart_discount_branches(cart_value, is_prime, coupon, expected):
    assert cart_discount(cart_value, is_prime, coupon) == expected


@pytest.mark.parametrize(
    "cart_value, is_prime, is_express, expected",
    [
        pytest.param(499, False, False, 40, id="paid-standard"),
        pytest.param(500, False, False, 0, id="free-standard"),
        pytest.param(100, True, False, 0, id="prime-standard"),
        pytest.param(499, False, True, 140, id="paid-express"),
        pytest.param(500, False, True, 100, id="free-base-express"),
        pytest.param(100, True, True, 50, id="prime-express"),
        pytest.param(500, True, False, 0, id="prime-at-free-shipping-threshold"),
        pytest.param(500, True, True, 50, id="prime-express-at-threshold"),
    ],
)
def test_shipping_branches(cart_value, is_prime, is_express, expected):
    assert shipping_fee(cart_value, is_prime, is_express) == expected
