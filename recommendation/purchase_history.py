import pandas as pd

from recommendation.model import products_df


def get_purchase_history(user_id, mysql):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT DISTINCT product_id
        FROM orders
        WHERE user_id=%s
        ORDER BY product_id DESC
        LIMIT 12
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()

    if not rows:
        return []

    purchased_ids = [

        row[0]

        for row in rows

    ]

    purchased_products = products_df[

        products_df['product_id']
        .isin(purchased_ids)

    ]

    purchased_products = purchased_products[

        purchased_products['image']
        .notna()

        &

        (~purchased_products['image']
         .str.contains(
            'default.jpg',
            case=False,
            na=False
         ))

    ]

    INNERWEAR = (
        "bra|brief|panty|lingerie|boxer|"
        "camisole|slip|petticoat|"
        "nightwear|innerwear|shapewear"
    )

    purchased_products = purchased_products[
        ~purchased_products["product_name"]
        .fillna("")
        .str.lower()
        .str.contains(INNERWEAR, regex=True)
    ]

    return purchased_products.to_dict(
        orient='records'
    )