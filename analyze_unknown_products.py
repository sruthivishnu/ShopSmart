import re
from collections import Counter

import pandas as pd

from recommendation.product_intelligence import detect_product_type

# ---------------------------------------
# LOAD PRODUCTS
# ---------------------------------------

products = pd.read_csv("products_fixed.csv")

products["product_name"] = (
    products["product_name"]
    .fillna("")
    .str.lower()
)

# ---------------------------------------
# FIND UNKNOWN PRODUCTS
# ---------------------------------------

unknown = products[
    products["product_name"].apply(
        lambda x: detect_product_type(x) == "other"
    )
]

print("Unknown Products :", len(unknown))

# ---------------------------------------
# WORD FREQUENCY
# ---------------------------------------

STOP_WORDS = {

    "for",
    "with",
    "and",
    "of",
    "the",
    "to",
    "in",
    "on",
    "by",
    "cm",
    "set",
    "combo",
    "pack",
    "piece",
    "pieces",
    "men",
    "women",
    "boys",
    "girls",
    "baby",
    "casual",
    "printed",
    "solid",
    "regular",
    "fit",
    "round",
    "neck",
    "full",
    "coverage",
    "analog",
    "digital",
    "black",
    "blue",
    "white",
    "red",
    "green",
    "pink",
    "yellow",
    "gold",
    "silver",
    "cotton"

}

counter = Counter()

for name in unknown["product_name"]:

    words = re.findall(r"[a-z0-9]+", name)

    for word in words:

        if len(word) < 3:
            continue

        if word in STOP_WORDS:
            continue

        counter[word] += 1

print("\nTop 200 Unknown Words\n")

for word, count in counter.most_common(200):

    print(f"{word:<20} {count}")