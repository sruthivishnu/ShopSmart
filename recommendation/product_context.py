from recommendation.model import products_df

from recommendation.product_intelligence import (
    detect_gender,
    detect_product_type,
    get_compatible_types,
    is_fashion
)


def build_product_context(product_id):
    """
    Builds a reusable context object for the selected product.

    Every recommendation engine
    (Similar Products, FBT, Trending)
    should use this context.
    """

    selected = products_df[
        products_df["product_id"] == product_id
    ]

    if selected.empty:
        return None

    product = selected.iloc[0]

    product_name = str(
        product["product_name"]
    )

    category = str(
        product["category"]
    ).lower().strip()

    gender = detect_gender(
        product_name
    )

    product_type = detect_product_type(
        product_name
    )

    compatible_types = get_compatible_types(
        product_type
    )

    return {

        "product": product,

        "product_id": int(product_id),

        "product_name": product_name,

        "category": category,

        "gender": gender,

        "product_type": product_type,

        "compatible_types": compatible_types,

        "is_fashion": is_fashion(category)

    }