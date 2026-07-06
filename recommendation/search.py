import re

from recommendation.model import products_df


# -----------------------------------
# CLEAN TEXT FUNCTION
# -----------------------------------

def clean(text):

    text = str(text).lower()

    text = re.sub(
        r'[^a-z0-9 ]',
        '',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    ).strip()

    return text


# -----------------------------------
# CREATE CLEAN COLUMN
# -----------------------------------

products_df['clean_name'] = (
    products_df['product_name']
    .apply(clean)
)


# -----------------------------------
# SEARCH FUNCTION
# -----------------------------------

def search_products(product_name):

    search_name = clean(product_name)

    # -----------------------------------
    # PARTIAL MATCHING
    # -----------------------------------

    matches = products_df[

        products_df['clean_name']
        .str.contains(
            search_name,
            na=False
        )

    ].copy()


    # -----------------------------------
    # PRIORITIZE BETTER MATCHES
    # -----------------------------------

    matches['priority'] = matches[
        'clean_name'
    ].apply(

        lambda x:
        x.startswith(search_name)

    )


    # -----------------------------------
    # PRIORITIZE PRODUCTS
    # WITH REAL IMAGES
    # -----------------------------------

    matches['has_real_image'] = (

        matches['image']
        != 'images/default.jpg'

    )


    # -----------------------------------
    # SORT RESULTS
    # -----------------------------------

    matches = matches.sort_values(
        by=[
            'priority',
            'has_real_image'
        ],
        ascending=False
    )

    # -----------------------------------
    # REMOVE DUPLICATE SEARCH RESULTS
    # -----------------------------------

    matches = matches.drop_duplicates(
        subset='clean_name'
    )

    # -----------------------------------
    # RETURN RESULTS
    # -----------------------------------

    return matches[
        [
            'product_id',
            'product_name',
            'image',
            'category',
            'price'
        ]
    ].head(20)