import json
import os
from flask import session
from modules.box__ecommerce.product.models import Product
from modules.box__ecommerce.category.models import Category
from modules.box__ecommerce.category.models import SubCategory
from modules.box__default.settings.helpers import get_setting

dirpath = os.path.dirname(os.path.abspath(__file__))
box_path = os.path.dirname(dirpath)


def get_currency_symbol():
    curr_code = get_setting("CURRENCY")
    with open(
        os.path.join(
            box_path,
            "shopman",
            "data",
            "currency.json",
        )
    ) as f:
        currencies = json.load(f)
    for curr in currencies:
        if curr["cc"] == curr_code:
            return curr["symbol"]


def get_cart_data():
    if "cart" in session:
        cart_data = session["cart"][0]
        cart_items = sum(cart_data.values())

        cart_total_price = 0
        try:
            for item in cart_data:
                print(item)
                product = Product.query.filter_by(barcode=item).first()
                cart_total_price += (
                    int(cart_data[item]) * product.selling_price
                )
        except Exception as e:
            pass

    else:
        session["cart"] = [{}]
        cart_data = session["cart"][0]
        cart_items = 0
        cart_total_price = 0

    return {
        "cart_data": cart_data,
        "cart_items": cart_items,
        "cart_total_price": cart_total_price,
    }


def get_min_max_subcateg(subcategory_name):
    subcateg = SubCategory.query.filter(SubCategory.name == subcategory_name).first()
    if len(subcateg.products) > 0:
        min_price = min((p.selling_price for p in subcateg.products))
        max_price = max((p.selling_price for p in subcateg.products))
    else:
        min_price = 0
        max_price = 2000
    return [min_price, max_price]