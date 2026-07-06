from flask import session
from recommendation.user_recommendation import (
    get_buy_again_products
)


def get_order_products():

    if "user_id" not in session:

        return []

    try:

        return get_buy_again_products(
            session["user_id"],
            top_n=5
        )

    except Exception as e:

        print("ORDER ERROR =", e)

        return []