import pandas as pd
import os
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommendation.product_intelligence import (
    detect_gender,
    detect_product_type,
    build_combined_features,
    get_canonical_category
)

import time

start = time.time()
print("Model loading started...")

# -----------------------------------
# BASE DIRECTORY
# -----------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# -----------------------------------
# FILE PATHS
# -----------------------------------
products_path = os.path.join(
    BASE_DIR,
    "products_cleaned.csv"
)

transactions_path = os.path.join(
    BASE_DIR,
    'transactions.csv'
)

users_path = os.path.join(
    BASE_DIR,
    'users.csv'
)

apriori_path = os.path.join(
    BASE_DIR,
    'transactions_apriori.csv'
)

images_folder = os.path.join(
    BASE_DIR,
    'static',
    'images'
)


# -----------------------------------
# LOAD DATASETS
# -----------------------------------

products_df = pd.read_csv(
    products_path
)


#print(products_df['subcategory'].drop_duplicates().head(50))

print("Products loaded:", round(time.time() - start, 2), "seconds")

products_df.fillna(
    '',
    inplace=True
)
products_df['search_text'] = (

    products_df['product_name']
    .fillna('')
    .astype(str)
    .str.lower()

    + ' ' +

    products_df['subcategory']
    .fillna('')
    .astype(str)
    .str.lower()

    + ' ' +

    products_df['category']
    .fillna('')
    .astype(str)
    .str.lower()

)

# -----------------------------------
# CLEAN CATEGORY
# -----------------------------------

products_df['category'] = (
    products_df['category']
    .astype(str)
    .str.lower()
)


# -----------------------------------
# LOAD IMAGE FILENAMES
# -----------------------------------
all_images = os.listdir(images_folder)

cleaned_image_map = {}

for image_file in all_images:

    clean_name = re.sub(
        r'[^a-z0-9]',
        '',
        os.path.splitext(image_file)[0].lower()
    )

    cleaned_image_map[clean_name] = image_file


# -----------------------------------
# IMAGE DETECTION FUNCTION
# -----------------------------------
def generate_image_path(product_name):

    key = re.sub(
        r'[^a-z0-9]',
        '',
        str(product_name).lower()
    )

    image = cleaned_image_map.get(key)

    if image:
        return "images/" + image

    return "images/default.jpg"


# -----------------------------------
# GENERATE IMAGE COLUMN
# -----------------------------------

products_df['image'] = (
    products_df['product_name']
    .apply(generate_image_path)
)

print("Images mapped:", round(time.time() - start, 2), "seconds")


# -----------------------------------
# REMOVE DUPLICATES
# -----------------------------------

products_df.drop_duplicates(
    subset='product_id',
    inplace=True
)


# -----------------------------------
# PRODUCT ID TYPE
# -----------------------------------

products_df['product_id'] = (
    products_df['product_id']
    .astype(int)
)


# -----------------------------------
# GENERATE REALISTIC PRICES
# -----------------------------------

def generate_price(category):

    category = str(category).lower()

    if 'clothing' in category:

        return random.randint(
            299,
            1999
        )

    elif 'footwear' in category:

        return random.randint(
            499,
            3999
        )

    elif 'watch' in category:

        return random.randint(
            599,
            9999
        )

    elif 'bag' in category:

        return random.randint(
            399,
            4999
        )

    elif 'electronics' in category:

        return random.randint(
            1999,
            49999
        )

    elif 'mobile' in category:

        return random.randint(
            6999,
            79999
        )

    elif 'laptop' in category:

        return random.randint(
            29999,
            149999
        )

    elif 'furniture' in category:

        return random.randint(
            1499,
            24999
        )

    else:

        return random.randint(
            199,
            2999
        )


products_df['price'] = (
    products_df['category']
    .apply(generate_price)
)


# -----------------------------------
# GENERATE REALISTIC RATINGS
# -----------------------------------

products_df['rating'] = [

    round(
        random.uniform(3.5, 5.0),
        1
    )

    for _ in range(len(products_df))

]


# -----------------------------------
# GENERATE REALISTIC REVIEWS
# -----------------------------------

products_df['reviews'] = [

    random.randint(10, 5000)

    for _ in range(len(products_df))

]


# -----------------------------------
# CREATE COMBINED FEATURES
# IMPORTANT FOR BETTER RECOMMENDATIONS
# -----------------------------------
# -----------------------------------
# EXTRACT GENDER TYPE
# -----------------------------------

# def detect_gender(product_name):
#
#     name = str(product_name).lower()
#
#     if 'women' in name or 'woman' in name or 'ladies' in name:
#
#         return 'women women women women women'
#
#     elif 'men' in name or 'man' in name:
#
#         return 'men men men men men'
#
#     elif 'boy' in name or 'boys' in name:
#
#         return 'boys boys boys boys'
#
#     elif 'girl' in name or 'girls' in name:
#
#         return 'girls girls girls girls'
#
#     elif 'kid' in name or 'kids' in name:
#
#         return 'kids kids kids kids'
#
#     else:
#
#         return ''



products_df["gender_feature"] = (
    products_df["product_name"]
    .apply(detect_gender)
)

print("Gender features created:", round(time.time() - start, 2), "seconds")

products_df["type_feature"] = (
    products_df["product_name"]
    .apply(detect_product_type)
)

# -----------------------------------
# CANONICAL CATEGORY
# -----------------------------------

products_df["canonical_category"] = (

    products_df.apply(

        lambda row:

        get_canonical_category(

            row["type_feature"],

            row["category"]

        ),

        axis=1

    )

)

print("Type features created:", round(time.time() - start, 2), "seconds")

# -----------------------------------
# CREATE STRONG COMBINED FEATURES
# -----------------------------------
products_df["combined_features"] = (
    products_df.apply(
        build_combined_features,
        axis=1
    )
)

print("Combined features created:", round(time.time() - start, 2), "seconds")

# -----------------------------------
# TF-IDF VECTORIZATION
# -----------------------------------

vectorizer = TfidfVectorizer(
    stop_words='english'
)

feature_vectors = vectorizer.fit_transform(
    products_df['combined_features']
)
print("TF-IDF completed:", round(time.time() - start, 2), "seconds")

# -----------------------------------
# FEATURE VECTORS READY
# Similarity will be calculated
# only when required.
# -----------------------------------

print(
    "Feature vectors ready:",
    round(time.time() - start, 2),
    "seconds"
)


# -----------------------------------
# LOAD OTHER DATASETS
# -----------------------------------

transactions_df = pd.read_csv(
    transactions_path
)

users_df = pd.read_csv(
    users_path
)

apriori_df = pd.read_csv(
    apriori_path
)


# -----------------------------------
# IMAGE COVERAGE CHECK
# -----------------------------------

real_images = products_df[
    products_df['image']
    != 'images/default.jpg'
]

print(
    '\nProducts with REAL images:',
    len(real_images)
)

print(
    '\nTotal products:',
    len(products_df)
)
print(
    '\nRecommendation model ready successfully!'
)
