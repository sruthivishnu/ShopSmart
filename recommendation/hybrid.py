import random
import re

from recommendation.model import (
    products_df
)

from recommendation.content import get_content_recommendations

from recommendation.apriori import (
    get_apriori_recommendations
)

from recommendation.category_cf import (
    category_based_recommendation
)

from recommendation.content import (
    get_content_recommendations
)

import pandas as pd

from recommendation.product_intelligence import (
    detect_product_type,
    get_compatible_types,
    detect_gender,
    is_fashion,
    normalize_text,
    same_brand_score,
    common_word_score,
    filter_compatible_products
)

from recommendation.product_context import (
    build_product_context
)

from recommendation.recommendation_validator import (
    prepare_recommendations,
    apply_gender_filter,
    filter_similar_products,
    filter_compatible_products,
    rank_products,
    rank_fbt_products
)

# -----------------------------------------
# REMOVE DUPLICATE PRODUCTS
# (handles same product with different IDs)
# -----------------------------------------

def remove_duplicate_product_names(df):

    if df.empty:
        return df

    df = df.copy()

    df["clean_name"] = (

        df["product_name"]

        .astype(str)

        .str.lower()

        .str.replace(r"[^a-z0-9]", "", regex=True)

    )

    # Keep highest rated version
    if "rating" in df.columns:

        df = (

            df

            .sort_values("rating", ascending=False)

            .drop_duplicates(
                subset="clean_name",
                keep="first"
            )

        )

    else:

        df = df.drop_duplicates(
            subset="clean_name"
        )

    return df.drop(columns="clean_name")

# -----------------------------------
# RECOMMENDATION HELPERS
# -----------------------------------

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

def remove_similar_duplicates(df, exclude_names=None):

    if df.empty:
        return df

    df = df.copy()

    if "product_name" not in df.columns:
        return df

    df["clean_name"] = (
        df["product_name"]
        .fillna("")
        .str.lower()
        .str.replace(r"[^a-z0-9 ]", "", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df = df.drop_duplicates(subset="clean_name")

    if exclude_names is not None:

        exclude_names = {
            str(x).lower().strip()
            for x in exclude_names
        }

        df = df[
            ~df["clean_name"].isin(exclude_names)
        ]

    return df.drop(columns=["clean_name"])

def get_fashion_categories():

    return {

        "clothing",
        "footwear",
        "bags, wallets & belts",
        "watches",
        "jewellery"

    }


# -----------------------------------
# HYBRID RECOMMENDATION
# -----------------------------------

def hybrid_recommendation(
        user_id,
        product_id,
        top_n=5
):

    recommendation_sections = {}

    # -----------------------------------
    # SELECT PRODUCT
    # -----------------------------------

    selected_product = products_df[

        products_df['product_id']
        == product_id

    ]

    if selected_product.empty:

        return {}

    selected_product = (
        selected_product.iloc[0]
    )
    selected_subcategory = str(
        selected_product['subcategory']
    ).lower()

    selected_category = str(
        selected_product['category']
    ).strip().lower()

    selected_name = str(
        selected_product['product_name']
    ).lower()

    selected_gender = normalize_text(
        selected_product["gender_feature"]
    )

    # Detect the product type from the product name first.
    # Falls back internally if needed.
    selected_type = detect_product_type(
        selected_product["product_name"]
    )

    # -----------------------------------------
    # SIMILAR PRODUCTS
    # -----------------------------------------

    selected_product = products_df[
        products_df["product_id"] == product_id
        ].iloc[0]

    selected_category = normalize_text(
        selected_product["category"]
    )

    selected_gender = normalize_text(
        selected_product["gender_feature"]
    )

    selected_type = detect_product_type(
        selected_product["product_name"]
    )

    # -----------------------------------------
    # BUILD CANDIDATE SET
    # -----------------------------------------

    similar_products = get_content_recommendations(
        product_id,
        top_n=100
    ).copy()

    print("CONTENT =", len(similar_products))

    # Fallback if content-based returns nothing
    if similar_products.empty:
        similar_products = products_df[
            products_df["category"]
            .fillna("")
            .apply(normalize_text)
            == selected_category
            ].copy()

    # Remove current product
    similar_products = similar_products[
        similar_products["product_id"] != product_id
    ]

    # -----------------------------------------
    # FILTER
    # -----------------------------------------

    similar_products = filter_similar_products(
        similar_products,
        selected_product
    )

    print("FILTER =", len(similar_products))

    # -----------------------------------------
    # CLEANUP
    # -----------------------------------------

    similar_products = prepare_recommendations(
        similar_products
    )

    print("PREPARE =", len(similar_products))

    # -----------------------------------------
    # RANK
    # -----------------------------------------

    similar_products = rank_products(
        similar_products,
        selected_product,
        selected_gender,
        selected_type
    )

    print("RANK =", len(similar_products))

    # -----------------------------------------
    # REMOVE DEFAULT IMAGES
    # -----------------------------------------

    similar_products = similar_products[
        similar_products["image"] != "images/default.jpg"
        ]

    similar_products = remove_duplicate_product_names(
        similar_products
    )

    print("IMAGE FILTER =", len(similar_products))

    # -----------------------------------------
    # FINAL GENDER VALIDATION
    # -----------------------------------------

    if (
            selected_category in get_fashion_categories()
            and selected_gender
    ):
        similar_products = similar_products[
            similar_products["gender_feature"]
            .fillna("")
            .str.lower()
            ==
            selected_gender.lower()
        ]

    # -----------------------------------------
    # FURNITURE CLEANUP
    # -----------------------------------------

    if selected_category == "furniture":
        # Keep only real furniture
        similar_products = similar_products[

            similar_products["product_name"]

            .str.contains(

                r"sofa|chair|table|desk|cabinet|wardrobe|"
                r"bookshelf|bookcase|dining|study table|"
                r"coffee table|tv unit|recliner",

                case=False,

                na=False,

                regex=True

            )

        ]

        # Remove home furnishing & pet items
        similar_products = similar_products[

            ~

            similar_products["product_name"]

            .str.contains(

                r"pet|dog|cat|rug|carpet|curtain|"
                r"bedsheet|blanket|pillow|cushion|"
                r"wall sticker|mat",

                case=False,

                na=False,

                regex=True

            )

        ]

    # -----------------------------------------
    # STORE CURRENT SIMILAR IDS
    # -----------------------------------------

    similar_products = similar_products.drop_duplicates(
        subset="product_name"
    )

    similar_products = similar_products[
        similar_products["image"] != "images/default.jpg"
        ]

    similar_ids = set(
        similar_products["product_id"].tolist()
    )

    # -----------------------------------------
    # FINAL
    # -----------------------------------------

    # -----------------------------------------
    # SMART REFILL
    # -----------------------------------------

    if len(similar_products) < top_n:

        needed = top_n - len(similar_products)

        extra = products_df.copy()

        # Same category only
        extra = extra[
            extra["category"]
            .fillna("")
            .apply(normalize_text)
            == selected_category
            ]

        # Remove already selected
        extra = extra[
            ~extra["product_id"].isin(
                similar_products["product_id"]
            )
        ]

        # Remove current product
        extra = extra[
            extra["product_id"] != product_id
            ]

        # Remove default image
        extra = extra[
            extra["image"] != "images/default.jpg"
            ]

        # Fashion gender
        if (
                selected_category in get_fashion_categories()
                and selected_gender
        ):
            extra = extra[
                extra["gender_feature"]
                .fillna("")
                .str.lower()
                ==
                selected_gender.lower()
                ]

        # -----------------------------------------
        # STRONGLY PREFER SAME PRODUCT TYPE
        # -----------------------------------------

        if selected_type:

            same_type = extra[
                extra["type_feature"]
                .fillna("")
                .str.lower()
                ==
                selected_type.lower()
                ]

            if len(same_type) >= needed:

                extra = same_type

            elif not same_type.empty:

                remaining = extra[
                    extra["type_feature"]
                    .fillna("")
                    .str.lower()
                    !=
                    selected_type.lower()
                    ]

                extra = pd.concat(
                    [same_type, remaining],
                    ignore_index=True
                )

        extra = rank_products(
            extra,
            selected_product,
            selected_gender,
            selected_type
        )

        similar_products = pd.concat(
            [
                similar_products,
                extra.head(needed)
            ]
        ).drop_duplicates(
            subset="product_id"
        )

    similar_products = similar_products.head(top_n)

    recommendation_sections[
        "Similar Products"
    ] = similar_products


    # -----------------------------------------
    # STORE FINAL SIMILAR IDS
    # -----------------------------------------

    similar_ids.update(
        similar_products["product_id"].tolist()
    )

    # Also store current product
    similar_ids.add(product_id)

    similar_names = set(

        similar_products["product_name"]

        .str.lower()

        .str.strip()

        .tolist()

    )

    similar_names.add(

        selected_product["product_name"]

        .lower()

        .strip()

    )


    # -----------------------------------------
    # APRIORI FREQUENTLY BOUGHT TOGETHER
    # -----------------------------------------

    # -----------------------------------------
    # STORE PRODUCT IDS FIRST
    # -----------------------------------------

    recommended_ids = []

    # -----------------------------------------
    # LEVEL 1 : APRIORI
    # -----------------------------------------

    # Get more candidates than we need
    apriori_ids = get_apriori_recommendations(
        product_id,
        top_n=15
    )

    print("APRIORI IDS =", apriori_ids)

    if apriori_ids:
        recommended_ids.extend(apriori_ids)

        print(
            "APRIORI PRODUCTS =",
            len(recommended_ids)
        )

    current_gender = selected_gender.lower().strip()
    current_type = selected_type.lower().strip()

    fashion_categories = get_fashion_categories()

    # --------------------------------------------------
    # CATEGORY BUNDLE ENGINE (FILL REMAINING SLOTS)
    # --------------------------------------------------

    if len(recommended_ids) < top_n:

        # -----------------------------------------
        # DETECT PRODUCT TYPE USING PRODUCT NAME
        # -----------------------------------------

        selected_product_type = detect_product_type(
            selected_product["product_name"]
        )

        compatible_types = get_compatible_types(
            selected_product_type
        )

        print("\nSELECTED PRODUCT")
        print(selected_product["product_name"])

        print("DETECTED TYPE =", selected_product_type)

        print("COMPATIBLE TYPES =", compatible_types)

        print("\nTYPE FEATURE COUNTS")
        print(
            products_df["type_feature"]
            .value_counts()
            .head(50)
        )

        if compatible_types:

            bundle_df = products_df[

                products_df["type_feature"]
                .fillna("")
                .str.lower()
                .isin(
                    [t.lower() for t in compatible_types]
                )

            ].copy()

            print(
                "COMPATIBLE PRODUCTS FOUND =",
                len(bundle_df)
            )

            # Remove current product
            # -----------------------------------------
            # BUNDLE SAFETY CHECK
            # -----------------------------------------

            if not bundle_df.empty and "product_id" in bundle_df.columns:

                bundle_df = bundle_df[
                    bundle_df["product_id"] != product_id
                    ]

            else:

                bundle_df = products_df.iloc[0:0].copy()

            # Remove products already returned by Apriori
            if recommended_ids:
                bundle_df = bundle_df[
                    ~bundle_df["product_id"].isin(
                        recommended_ids
                    )
                ]

            # Gender filter for fashion products
            if selected_category in fashion_categories and current_gender:
                bundle_df = bundle_df[
                    bundle_df["gender_feature"]
                    .fillna("")
                    .str.lower()
                    .str.contains(current_gender, na=False)
                ]

            # Prefer better bundle products

            bundle_df = bundle_df[
                bundle_df["image"] != "images/default.jpg"
                ]

            bundle_df = remove_duplicate_product_names(bundle_df)

            bundle_df = filter_compatible_products(
                bundle_df,
                selected_product
            )

            bundle_df = rank_products(
                bundle_df,
                selected_product,
                current_gender,
                selected_product_type
            )

            needed = top_n - len(recommended_ids)

            balanced_rows = []

            used_ids = set()

            # -----------------------------------------
            # Take up to TWO products from each type
            # -----------------------------------------

            for product_type in compatible_types:

                group = bundle_df[
                    bundle_df["type_feature"]
                    .str.lower()
                    == product_type.lower()
                    ].head(2)

                for _, row in group.iterrows():

                    if row["product_id"] not in used_ids:
                        balanced_rows.append(row)

                        used_ids.add(row["product_id"])

            # -----------------------------------------
            # Fill remaining slots
            # -----------------------------------------

            if len(balanced_rows) < needed:

                remaining = bundle_df[
                    ~bundle_df["product_id"].isin(used_ids)
                ]

                for _, row in remaining.iterrows():

                    if len(balanced_rows) >= needed:
                        break

                    balanced_rows.append(row)

            bundle_df = pd.DataFrame(balanced_rows)

            recommended_ids.extend(
                bundle_df["product_id"].tolist()
            )

            print("\nBALANCED BUNDLE")
            print(
                bundle_df[
                    ["product_name", "type_feature"]
                ]
            )

            print("BUNDLE ADDED =", len(bundle_df))

    # -----------------------------------------
    # FALLBACK TO SAME CATEGORY
    # -----------------------------------------

    if len(recommended_ids) < top_n:

        category_df = products_df[

            products_df["category"]
            .fillna("")
            .str.lower()
            == selected_category.lower()

            ].copy()

        category_df = category_df[
            category_df["product_id"] != product_id
            ]

        category_df = category_df[
            ~category_df["product_id"].isin(
                recommended_ids
            )
        ]

        if current_gender:
            category_df = category_df[
                category_df["gender_feature"]
                .fillna("")
                .str.lower()
                .str.contains(current_gender, na=False)
            ]

        category_df = category_df[
            category_df["image"] != "images/default.jpg"
            ]

        category_df = remove_duplicate_product_names(category_df)

        category_df = filter_compatible_products(
            category_df,
            selected_product
        )

        category_df = rank_products(
            category_df,
            selected_product,
            current_gender,
            selected_product_type
        )

        needed = top_n - len(recommended_ids)

        recommended_ids.extend(
            category_df.head(needed)["product_id"].tolist()
        )

        print("CATEGORY FALLBACK =", min(needed, len(category_df)))

    # --------------------------------------------------
    # BUILD DATAFRAME FROM FINAL IDS
    # --------------------------------------------------

    # Remove duplicates while preserving order
    recommended_ids = list(dict.fromkeys(recommended_ids))

    # Remove current product if present
    recommended_ids = [
        pid for pid in recommended_ids
        if pid != product_id
    ]

    # Limit recommendations
    recommended_ids = recommended_ids[:top_n]

    # Build DataFrame only once
    frequently_bought = products_df[
        products_df["product_id"].isin(recommended_ids)
    ].copy()

    # -----------------------------------------
    # REMOVE PRODUCTS ALREADY SHOWN
    # IN SIMILAR PRODUCTS
    # -----------------------------------------

    # -----------------------------------------
    # REMOVE PRODUCTS ALREADY SHOWN
    # -----------------------------------------

    frequently_bought = frequently_bought[

        ~frequently_bought["product_id"].isin(
            similar_ids
        )

    ].copy()

    # -----------------------------------------
    # KEEP ONLY COMPATIBLE TYPES
    # NEVER RETURN SAME PRODUCT TYPE
    # -----------------------------------------

    if not frequently_bought.empty:

        compatible_types = [
            t.lower()
            for t in get_compatible_types(selected_type)
        ]

        if compatible_types:
            frequently_bought = frequently_bought[

                frequently_bought["type_feature"]
                .fillna("")
                .str.lower()
                .isin(compatible_types)

            ].copy()

            # Remove the same type as the selected product
            frequently_bought = frequently_bought[

                frequently_bought["type_feature"]
                .fillna("")
                .str.lower()

                != selected_type.lower()

                ]

    print("AFTER COMPATIBILITY =", len(frequently_bought))
    print(
        frequently_bought[
            ["product_name", "type_feature"]
        ]
    )

    # --------------------------------------------------
    # LEVEL 3 : FASHION FILTERS
    # --------------------------------------------------

    if (
            selected_category in fashion_categories
            and not frequently_bought.empty
    ):

        if current_gender:

            gender_filtered = frequently_bought[
                frequently_bought["gender_feature"]
                .fillna("")
                .str.lower()
                ==
                current_gender
            ]

            if not gender_filtered.empty:
                frequently_bought = gender_filtered

    # --------------------------------------------------
    # CLEANUP
    # --------------------------------------------------

    if not frequently_bought.empty:

        frequently_bought = frequently_bought[

            frequently_bought["image"] != "images/default.jpg"

            ]

        print("IMAGE =", len(frequently_bought))

        frequently_bought = remove_duplicate_product_names(
            frequently_bought
        )

        print("REMOVE DUPLICATES =", len(frequently_bought))

        # -----------------------------------------
        # KEEP ONLY ONE PRODUCT PER TYPE
        # -----------------------------------------

        if not frequently_bought.empty:
            frequently_bought = (
                frequently_bought
                .groupby("type_feature", group_keys=False)
                .head(2)
                .reset_index(drop=True)
            )

        print("TYPE DEDUP =", len(frequently_bought))

        frequently_bought = filter_compatible_products(
            frequently_bought,
            selected_product
        )

        print("FILTER COMPATIBLE =", len(frequently_bought))

        frequently_bought = rank_fbt_products(
            frequently_bought,
            selected_product,
            current_gender,
            selected_product_type
        )

        print("RANK FBT =", len(frequently_bought))

        # -----------------------------------------
        # FILL REMAINING SLOTS
        # -----------------------------------------

        if len(frequently_bought) < top_n:

            needed = top_n - len(frequently_bought)

            extra = products_df[

                products_df["category"]
                .fillna("")
                .str.lower()
                ==
                selected_category.lower()

                ].copy()

            extra = extra[
                ~extra["product_id"].isin(
                    frequently_bought["product_id"]
                )
            ]

            extra = extra[
                ~extra["product_id"].isin(
                    similar_ids
                )
            ]

            extra = extra[
                extra["image"] != "images/default.jpg"
                ]

            if current_gender:
                extra = extra[
                    extra["gender_feature"]
                    .fillna("")
                    .str.lower()
                    ==
                    current_gender
                    ]

            extra = rank_products(

                extra,

                selected_product,

                current_gender,

                selected_product_type

            )

            frequently_bought = pd.concat(

                [

                    frequently_bought,

                    extra.head(needed)

                ]

            ).drop_duplicates(
                subset="product_id"
            )

        # -----------------------------------------
        # FILL REMAINING SLOTS USING CONTENT ENGINE
        # -----------------------------------------

        if len(frequently_bought) < top_n:
            needed = top_n - len(frequently_bought)

            content_df = get_content_recommendations(
                product_id,
                top_n=100
            )

            # -----------------------------------------
            # REMOVE ALREADY DISPLAYED PRODUCTS
            # -----------------------------------------

            content_df = content_df[

                ~content_df["product_id"].isin(
                    similar_ids
                )

            ]

            content_df = content_df[

                ~content_df["product_id"].isin(
                    frequently_bought["product_id"]
                )

            ]

            content_df = content_df[

                content_df["product_id"] != product_id

                ]

            content_df = content_df[

                content_df["image"] != "images/default.jpg"

                ]

            content_df = filter_compatible_products(
                content_df,
                selected_product
            )

            content_df = remove_duplicate_product_names(
                content_df
            )

            content_df = rank_fbt_products(
                content_df,
                selected_product,
                current_gender,
                selected_product_type
            )

            # -----------------------------------------
            # FINAL GENDER FILTER
            # -----------------------------------------

            if (
                    selected_category in fashion_categories
                    and current_gender
            ):
                content_df = content_df[
                    content_df["gender_feature"]
                    .fillna("")
                    .str.lower()
                    ==
                    current_gender
                    ]

            frequently_bought = pd.concat(

                [

                    frequently_bought,

                    content_df.head(needed)

                ],

                ignore_index=True

            )

        frequently_bought = remove_similar_duplicates(
            frequently_bought
        )

        frequently_bought = frequently_bought.head(top_n)

    else:

        frequently_bought = products_df.iloc[0:0].copy()

    print("FINAL FBT =", len(frequently_bought))

    # -----------------------------------------
    # FINAL SAFETY
    # -----------------------------------------

    frequently_bought = frequently_bought[

        ~frequently_bought["product_id"].isin(
            similar_ids
        )

    ]

    frequently_bought = frequently_bought[

        frequently_bought["product_id"] != product_id

        ]

    frequently_bought = remove_similar_duplicates(

        frequently_bought,

        exclude_names=similar_names

    )

    frequently_bought = frequently_bought.head(top_n)

    recommendation_sections[
        "Frequently Bought Together"
    ] = frequently_bought

    # -----------------------------------------
    # TRENDING PRODUCTS
    # -----------------------------------------

    trending_df = products_df.copy()

    # -----------------------------------------
    # SAME CATEGORY
    # -----------------------------------------

    trending_df = trending_df[

        trending_df["category"]

        .fillna("")

        .apply(normalize_text)

        ==

        selected_category

        ]

    # -----------------------------------------
    # FASHION GENDER FILTER
    # -----------------------------------------

    if (

            selected_category in get_fashion_categories()

            and

            selected_gender

    ):
        trending_df = trending_df[

            trending_df["gender_feature"]

            .fillna("")

            .str.lower()

            ==

            selected_gender.lower()

            ]

    # -----------------------------------------
    # PREFER SAME TYPE
    # -----------------------------------------

    if selected_type:
        same_type = trending_df[

            trending_df["type_feature"]

            .fillna("")

            .str.lower()

            ==

            selected_type.lower()

            ]

        other_type = trending_df[

            trending_df["type_feature"]

            .fillna("")

            .str.lower()

            !=

            selected_type.lower()

            ]

        trending_df = pd.concat(

            [

                same_type,

                other_type

            ]

        )

    # -----------------------------------------
    # REMOVE CURRENT PRODUCT
    # -----------------------------------------

    trending_df = trending_df[

        trending_df["product_id"] != product_id

        ]

    # -----------------------------------------
    # REMOVE PRODUCTS ALREADY SHOWN
    # -----------------------------------------

    shown_ids = set()

    shown_ids.update(

        similar_products["product_id"].tolist()

    )

    shown_ids.update(

        frequently_bought["product_id"].tolist()

    )

    trending_df = trending_df[

        ~

        trending_df["product_id"].isin(shown_ids)

    ]

    # -----------------------------------------
    # REMOVE NO IMAGE
    # -----------------------------------------

    trending_df = trending_df[

        trending_df["image"]

        !=

        "images/default.jpg"

        ]

    # -----------------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------------

    trending_df = remove_duplicate_product_names(

        trending_df

    )

    # -----------------------------------------
    # RANK PRODUCTS
    # -----------------------------------------

    trending_df = rank_products(

        trending_df,

        selected_product,

        selected_gender,

        selected_type

    )

    # -----------------------------------------
    # FALLBACK
    # -----------------------------------------

    if len(trending_df) < top_n:
        extra = products_df[

            products_df["image"]

            !=

            "images/default.jpg"

            ]

        extra = extra[

            ~

            extra["product_id"].isin(

                shown_ids

            )

        ]

        extra = extra[

            extra["product_id"]

            !=

            product_id

            ]

        extra = remove_duplicate_product_names(

            extra

        )

        trending_df = pd.concat(

            [

                trending_df,

                extra

            ]

        )

    trending_df = trending_df.head(top_n)

    recommendation_sections[
        "Trending Products"
    ] = trending_df


    return recommendation_sections