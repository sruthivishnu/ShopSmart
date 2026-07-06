import pandas as pd

from recommendation.product_intelligence import (
    normalize_text,
    detect_product_type,
    detect_gender,
    is_innerwear,
    same_brand_score,
    common_word_score,
    get_compatible_types
)

INNERWEAR_KEYWORDS = [

    "bra",
    "brief",
    "briefs",
    "panty",
    "panties",
    "lingerie",
    "innerwear",
    "boxer",
    "boxers",
    "camisole",
    "slip",
    "petticoat",
    "nightwear",
    "shapewear"

]


def remove_default_images(df):

    if df.empty:
        return df

    return df[
        df["image"] != "images/default.jpg"
    ].copy()


def remove_innerwear(df):

    if df.empty:
        return df

    pattern = "|".join(INNERWEAR_KEYWORDS)

    return df[
        ~df["product_name"]
        .fillna("")
        .str.lower()
        .str.contains(
            pattern,
            regex=True
        )
    ].copy()

def remove_duplicate_products(df):

    if df.empty:
        return df

    df = df.copy()

    df["clean_name"] = (

        df["product_name"]

        .fillna("")

        .str.lower()

        .str.replace(r"[^a-z0-9 ]", "", regex=True)

        .str.replace(r"\s+", " ", regex=True)

        .str.strip()

    )

    df = df.drop_duplicates(
        subset="clean_name"
    )

    return df.drop(columns=["clean_name"])


def apply_gender_filter(df, gender):

    if df.empty:
        return df

    gender = str(gender).lower().strip()

    if gender == "":
        return df

    filtered = df[

        df["gender_feature"]

        .fillna("")

        .str.lower()

        .str.contains(
            gender,
            na=False
        )

    ]

    if filtered.empty:
        return df

    return filtered


def sort_products(df):

    if df.empty:
        return df

    return df.sort_values(

        by=[
            "rating",
            "reviews"
        ],

        ascending=False

    )


def prepare_recommendations(df):

    if df.empty:
        return df

    df = remove_default_images(df)

    df = remove_innerwear(df)

    df = remove_duplicate_products(df)

    df = sort_products(df)

    return df.reset_index(drop=True)

# ==========================================================
# FILTER SIMILAR PRODUCTS
# ==========================================================

def filter_similar_products(products, selected_product):

    if products.empty:
        return products

    selected_gender = normalize_text(
        selected_product["gender_feature"]
    )

    selected_category = normalize_text(
        selected_product["category"]
    )

    selected_type = detect_product_type(
        selected_product["product_name"]
    )

    print("\n===== SIMILAR FILTER DEBUG =====")
    print("Selected Category :", selected_category)
    print("Selected Gender   :", selected_gender)
    print("Initial Count     :", len(products))

    products = products[
        products["category"]
        .fillna("")
        .apply(normalize_text)
        == selected_category
    ]

    print("After Category :", len(products))

    if selected_gender != "":

        products = apply_gender_filter(
            products,
            selected_gender
        )

    print("After Gender :", len(products))

    # -----------------------------------------
    # SAME PRODUCT TYPE FILTER
    # -----------------------------------------

    if selected_type:

        same_type = products[

            products["product_name"]

            .apply(detect_product_type)

            ==

            selected_type

            ]

        # Only enforce if enough products exist
        if len(same_type) >= 4:
            products = same_type

            print("After Type :", len(products))

        # -----------------------------------------
        # SHIRT / T-SHIRT SAFETY FILTER
        # -----------------------------------------

        if selected_type and selected_type.lower() == "shirt":
            products = products[
                ~products["product_name"]
                .fillna("")
                .str.lower()
                .str.contains(
                    r"\bt-?shirt\b|\btshirt\b",
                    regex=True,
                    na=False
                )
            ]

            print("After Shirt Cleanup :", len(products))

    return products

# ==========================================================
# FILTER COMPATIBLE PRODUCTS
# ==========================================================

def filter_compatible_products(products, selected_product):

    if products.empty:
        return products

    products = products.copy()

    selected_gender = normalize_text(
        selected_product["gender_feature"]
    )

    # ---------------------------------
    # REMOVE CURRENT PRODUCT
    # ---------------------------------

    products = products[
        products["product_id"]
        != selected_product["product_id"]
    ]

    # ---------------------------------
    # REMOVE INNERWEAR
    # ---------------------------------

    products = products[
        ~products["product_name"]
        .apply(is_innerwear)
    ]

    # ---------------------------------
    # GENDER FILTER
    # ---------------------------------

    if selected_gender != "":

        products = apply_gender_filter(
            products,
            selected_gender
        )

    return products.reset_index(drop=True)

# ==========================================================
# SMART RANKING ENGINE
# ==========================================================

def rank_products(
        products,
        selected_product,
        selected_gender,
        selected_type
):

    if products.empty:
        return products

    products = products.copy()

    selected_name = normalize_text(
        selected_product["product_name"]
    )

    compatible_types = get_compatible_types(
        selected_type
    )

    products["detected_type"] = (
        products["product_name"]
        .apply(detect_product_type)
    )

    def score(product_type):

        if product_type == selected_type:
            return 100

        if product_type in compatible_types:
            return 60

        return 0

    products["type_score"] = (
        products["detected_type"]
        .apply(score)
    )

    products["brand_score"] = (
        products["product_name"]
        .apply(
            lambda x:
            same_brand_score(
                selected_name,
                x
            )
        )
    )

    products["word_score"] = (
        products["product_name"]
        .apply(
            lambda x:
            common_word_score(
                selected_name,
                x
            )
        )
    )

    products["gender_score"] = (
        products["gender_feature"]
        .fillna("")
        .str.lower()
        .str.contains(
            selected_gender,
            na=False
        )
        .astype(int)
        * 40
    )

    products["final_score"] = (

        products["type_score"]

        + products["gender_score"]

        + products["brand_score"]

        + products["word_score"] * 5

        + products["rating"] * 5

        + products["reviews"] / 100

    )

    return products.sort_values(

        "final_score",

        ascending=False

    )

# ==========================================================
# SMART RANKING FOR FREQUENTLY BOUGHT TOGETHER
# ==========================================================

def rank_fbt_products(
        products,
        selected_product,
        selected_gender,
        selected_type
):

    if products.empty:
        return products

    products = products.copy()

    compatible_types = get_compatible_types(
        selected_type
    )

    # ------------------------------------
    # TYPE SCORE
    # ------------------------------------

    products["type_score"] = products["type_feature"].apply(

        lambda x: 100
        if x in compatible_types
        else 0

    )

    # ------------------------------------
    # GENDER SCORE
    # ------------------------------------

    if selected_gender != "":

        products["gender_score"] = (

            products["gender_feature"]

            .fillna("")

            .str.lower()

            .str.contains(
                selected_gender,
                na=False
            )

            .astype(int)

            * 30

        )

    else:

        products["gender_score"] = 0

    # ------------------------------------
    # IMAGE SCORE
    # ------------------------------------

    products["image_score"] = (

        products["image"]

        != "images/default.jpg"

    ).astype(int) * 20

    # ------------------------------------
    # FINAL SCORE
    # ------------------------------------

    products["final_score"] = (

        products["type_score"]

        + products["gender_score"]

        + products["image_score"]

        + products["rating"] * 10

        + products["reviews"] / 50

    )

    return products.sort_values(

        "final_score",

        ascending=False

    )