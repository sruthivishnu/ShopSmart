import re

from recommendation.model import products_df

import pandas as pd

# -----------------------------------
# COMMON HOMEPAGE DATASET
# -----------------------------------

def get_homepage_products():

    valid_products = products_df[
        products_df["image"].notna()
    ]

    valid_products = valid_products[
        valid_products["image"] != "images/default.jpg"
    ]

    homepage_products = valid_products[

        ~

        valid_products["product_name"]
        .str.contains(
            r"bra|lingerie|innerwear|underwear|panty|brief|camisole|sports bra|bellies|ballerina|t-shirt bra|t-shirtbra|shapewear|thermal",
            case=False,
            na=False,
            regex=True
        )

    ]

    homepage_products = homepage_products.drop_duplicates(
        subset="product_id"
    )

    return homepage_products.reset_index(drop=True)

# -----------------------------------
# REMOVE DUPLICATE PRODUCTS
# -----------------------------------

def remove_duplicate_products(df):

    df = df.copy()

    df["clean_name"] = (

        df["product_name"]

        .str.lower()

        .str.replace(
            r"\s+",
            " ",
            regex=True
        )

        .str.strip()

    )

    df = df.drop_duplicates(
        subset="clean_name"
    )

    return df.drop(
        columns="clean_name"
    )

# -----------------------------------
# SELECT PRODUCTS
# -----------------------------------

def select_products(
        df,
        used_ids=None,
        limit=4
):

    if used_ids is None:
        used_ids = set()

    # -----------------------------------
    # REMOVE ALREADY USED PRODUCTS
    # -----------------------------------

    df = df[
        ~df["product_id"].isin(used_ids)
    ]

    # -----------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------

    df = remove_duplicate_products(df)

    selected = (

        df

        .sort_values(
            by="rating",
            ascending=False
        )

        .drop_duplicates(
            subset="product_name"
        )

        .head(limit)

    )

    # -----------------------------------
    # STORE USED IDS
    # -----------------------------------

    used_ids.update(
        selected["product_id"].tolist()
    )

    return (
        selected.to_dict("records"),
        used_ids
    )

# -----------------------------------
# HOT PICKS
# -----------------------------------

# -----------------------------------
# HOT PICKS
# -----------------------------------

def get_hot_picks(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        homepage_products["product_name"]

        .str.contains(

            r"\bshirt\b|dress|kurta|jeans|watch|shoe|sneaker|\bheel\b|bag|\bhandbag\b|backpack|wallet|jacket",

            case=False,

            na=False,

            regex=True

        )

    ]

    return select_products(
        filtered,
        used_ids
    )


# -----------------------------------
# DEALS UNDER ₹2000
# -----------------------------------

def get_top_deals(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        (homepage_products["price"] < 2000)

        &

        homepage_products["product_name"]

        .str.contains(

            r"dress|kurta|jeans|watch|shoe|sandal|bag|perfume|lipstick",

            case=False,

            na=False,

            regex=True

        )

    ]

    return select_products(
        filtered,
        used_ids
    )

# -----------------------------------
# FASHION DEALS
# -----------------------------------

def get_fashion_deals(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        (

            homepage_products["price"] < 3000

        )

        &

        (

            homepage_products["product_name"]

            .str.contains(

                r"shirt|dress|top|kurta|jeans|tshirt|shoe|sandal|bag",

                case=False,

                na=False,

                regex=True

            )

        )

    ]

    return select_products(
        filtered,
        used_ids
    )

# -----------------------------------
# TRENDING FOOTWEAR
# -----------------------------------

def get_footwear_products(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        homepage_products["product_name"]

        .str.contains(
            r"\brunning shoe\b|\bcasual shoe\b|\bsneaker\b|\bboot\b|\bheel\b|\bsandal\b",
            case=False,
            na=False,
            regex=True
        )

    ]

    filtered = filtered[
        ~filtered["product_name"].str.contains(
            r"bike|motorcycle|cover|tyre|tire|helmet|vehicle|wheel",
            case=False,
            regex=True,
            na=False
        )
    ]

    return select_products(
        filtered,
        used_ids
    )

# -----------------------------------
# BAGS & WALLETS
# -----------------------------------

def get_bags_products(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        homepage_products["product_name"]

        .str.contains(
            r"backpack|handbag|shoulder bag|sling bag|laptop bag",
            case=False,
            na=False,
            regex=True
        )

    ]

    return select_products(
        filtered,
        used_ids
    )

# -----------------------------------
# FURNITURE
# -----------------------------------

def get_furniture_products(
        used_ids=None
):

    homepage_products = get_homepage_products()

    # -----------------------------------
    # SOFAS
    # -----------------------------------

    sofas = homepage_products[

        homepage_products["product_name"]

        .str.contains(
            r"sofa|recliner|couch",
            case=False,
            na=False,
            regex=True
        )

    ]

    sofas = sofas[

        ~

        sofas["product_name"]

        .str.contains(
            r"baby|kid|kids|child|toy|pet",
            case=False,
            na=False,
            regex=True
        )

    ]

    sofas = sofas.drop_duplicates(
        subset="product_name"
    ).head(2)

    # -----------------------------------
    # CHAIRS
    # -----------------------------------

    chairs = homepage_products[

        homepage_products["product_name"]

        .str.contains(
            r"chair|armchair|dining chair|office chair|wooden chair",
            case=False,
            na=False,
            regex=True
        )

    ]

    # Remove kids / toy / inflatable chairs
    chairs = chairs[

        ~

        chairs["product_name"]

        .str.contains(
            r"baby|kid|kids|child|toy|inflatable|pet",
            case=False,
            na=False,
            regex=True
        )

    ]

    chairs = chairs.drop_duplicates(
        subset="product_name"
    ).head(2)
    selected = pd.concat([

        sofas,

        chairs

    ])

    if used_ids is None:
        used_ids = set()

    selected = selected[
        ~selected["product_id"].isin(used_ids)
    ]

    used_ids.update(
        selected["product_id"].tolist()
    )

    return (
        selected.to_dict("records"),
        used_ids
    )

# -----------------------------------
# PREMIUM WATCHES
# -----------------------------------

def get_watch_products(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        homepage_products["category"]

        .str.contains(
            "watches",
            case=False,
            na=False
        )

        &

        ~

        homepage_products["product_name"]

        .str.contains(
            r"kids|boy|girl|cartoon|character|box|case|storage|organizer|display|gift box|watch box|strap",
            case=False,
            na=False,
            regex=True
        )

    ]



    return select_products(
        filtered,
        used_ids
    )

# -----------------------------------
# BEAUTY PRODUCTS
# -----------------------------------

def get_beauty_products(
        used_ids=None
):

    homepage_products = get_homepage_products()

    filtered = homepage_products[

        (

            homepage_products["product_name"]

            .str.contains(

                r"perfume|fragrance|lipstick|makeup|cosmetic|face wash|conditioner|cream|lotion|beauty",

                case=False,

                na=False,

                regex=True

            )

        )

        |

        (

            homepage_products["category"]

            .str.contains(

                r"beauty|personal care",

                case=False,

                na=False,

                regex=True

            )

        )

    ]



    return select_products(
        filtered,
        used_ids
    )

