import pandas as pd

# ---------------------------------
# LOAD PRODUCTS
# ---------------------------------

products = pd.read_csv("products.csv")

print("Products Loaded :", len(products))

products["category"] = (
    products["category"]
    .fillna("")
    .str.strip()
    .str.lower()
)

products["product_name"] = (
    products["product_name"]
    .fillna("")
    .str.lower()
)

# ---------------------------------
# VALID CATEGORIES
# ---------------------------------

VALID_CATEGORIES = {

    "clothing",
    "footwear",
    "bags, wallets & belts",
    "watches",
    "jewellery",
    "beauty and personal care",
    "sports & fitness",
    "mobiles & accessories",
    "computers",
    "automotive",
    "baby care",
    "home furnishing",
    "home decor & festive needs",
    "home improvement",
    "home & kitchen",
    "kitchen & dining",
    "pet supplies",
    "furniture",
    "tools & hardware",
    "pens & stationery",
    "ebooks",
    "eyewear",
    "gaming",
    "cameras & accessories",
    "toys & school supplies",
    "food & nutrition",
    "health & personal care appliances",
    "wearable smart devices",
    "automation & robotics",
    "household supplies",
    "sunglasses"
}

# ---------------------------------
# INVALID CATEGORY COUNT
# ---------------------------------

invalid = products[
    ~products["category"].isin(VALID_CATEGORIES)
]

print()

print("INVALID CATEGORY COUNT =", len(invalid))

print()

print(

    invalid[
        ["product_name", "category"]
    ].head(50)

)

# ---------------------------------
# CATEGORY KEYWORD MAPPING
# ---------------------------------

CATEGORY_MAP = {

    "clothing": [
        "shirt", "t-shirt", "tshirt", "kurta", "kurti",
        "jeans", "leggings", "dress", "top",
        "bra", "panty", "blazer", "waistcoat",
        "jacket", "sweater", "cardigan",
        "cargo", "shorts", "trouser",
        "camisole", "vest", "saree",
        "lehenga", "salwar", "stole"
    ],

    "footwear": [
        "shoe", "shoes", "heels", "bellies",
        "boots", "sandals", "slippers",
        "flats", "wedges", "clogs",
        "running shoes", "lace up"
    ],

    "bags, wallets & belts": [
        "bag", "wallet", "belt",
        "clutch", "backpack",
        "handbag", "pouch"
    ],

    "jewellery": [
        "ring", "necklace", "bangle",
        "earring", "cufflink",
        "jewellery", "bracelet"
    ],

    "watches": [
        "watch"
    ],

    "mobiles & accessories": [
        "mobile", "phone", "lcd",
        "battery", "headset",
        "charger", "back panel"
    ],

    "baby care": [
        "baby", "girl", "boy"
    ],

    "sports & fitness": [
        "cricket", "skates",
        "running", "fitness"
    ]
}

# ---------------------------------
# SPECIAL PRODUCT MAPPING
# ---------------------------------

SPECIAL_MAP = {

    "artificial plant": "home decor & festive needs",
    "showpiece": "home decor & festive needs",
    "paper sky lantern": "home decor & festive needs",

    "motion sensor": "home improvement",
    "pump controller": "home improvement",
    "surge protector": "home improvement",
    "nail cutter": "home improvement",

    "car grill": "automotive",
    "sun shade": "automotive",
    "air filter": "automotive",

    "table cover": "home furnishing",
    "sofa cover": "home furnishing",

    "amplifier": "home entertainment",
    "speaker": "home entertainment",
    "sound bar": "home entertainment",
    "sub woofer": "home entertainment",

    "keyboard": "computers",

    "paper weight": "pens & stationery",
    "self stick": "pens & stationery",

    "boxer": "clothing",
    "brief": "clothing",
    "jumpsuit": "clothing",

    "baby walker": "baby care",

    "thigh guard": "sports & fitness"
}

# ---------------------------------
# FIX INVALID CATEGORIES
# ---------------------------------

fixed = 0

for idx in invalid.index:

    name = products.loc[idx, "product_name"]

    for category, keywords in CATEGORY_MAP.items():

        if any(word in name for word in keywords):

            products.loc[idx, "category"] = category

            fixed += 1

            break

print("\nTOTAL FIXED =", fixed)

remaining = products[
    ~products["category"].isin(VALID_CATEGORIES)
]

print("REMAINING INVALID =", len(remaining))

print(
    remaining[
        ["product_name", "category"]
    ].head(30)
)

# ---------------------------------
# SECOND PASS
# ---------------------------------

for idx in remaining.index:

    name = products.loc[idx, "product_name"]

    for keyword, category in SPECIAL_MAP.items():

        if keyword in name:

            products.loc[idx, "category"] = category

            break

remaining = products[
    ~products["category"].isin(VALID_CATEGORIES)
]

print("\nFINAL REMAINING =", len(remaining))

print(
    remaining[
        ["product_name", "category"]
    ].head(20)
)

products.to_csv(
    "products_fixed.csv",
    index=False
)

print("\nproducts_fixed.csv created successfully.")