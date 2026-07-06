import pandas as pd
from recommendation.product_intelligence import detect_product_type
# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("products.csv")

df.fillna("", inplace=True)

# -----------------------------
# VALID CATEGORIES
# -----------------------------

VALID_CATEGORIES = {

    "clothing",
    "footwear",
    "jewellery",
    "bags, wallets & belts",
    "beauty and personal care",
    "mobiles & accessories",
    "automotive",
    "home furnishing",
    "home decor & festive needs",
    "furniture",
    "sports & fitness",
    "watches",
    "baby care",
    "kitchen & dining",
    "pens & stationery",
    "tools & hardware",
    "computers",
    "cameras & accessories",
    "gaming",
    "ebooks",
    "pet supplies",
    "eyewear",
    "sunglasses",
    "toys & school supplies",
    "home entertainment",
    "health & personal care appliances",
    "home improvement",
    "home & kitchen"
}

# -----------------------------
# CATEGORY KEYWORDS
# -----------------------------

CATEGORY_RULES = {

    "clothing": [
        "shirt","tshirt","t-shirt","jeans","kurta","dress",
        "leggings","top","skirt","blouse","waistcoat",
        "dupatta","lehenga","saree","nightwear",
        "bra","panty","brief","innerwear",
        "shorts","trouser","trackpant","cargos",
        "hoodie","sweater","jacket"
    ],

    "footwear":[
        "shoe","shoes","sandal","slipper",
        "heel","bellies","clogs","boot",
        "loafer","canvas","flip flop","wedge"
    ],

    "jewellery":[
        "ring","necklace","earring",
        "bangle","bracelet","pendant"
    ],

    "bags, wallets & belts":[
        "bag","wallet","backpack",
        "handbag","belt","sling"
    ],

    "watches":[
        "watch"
    ],

    "furniture":[
        "sofa","chair","table","bed",
        "wardrobe","stool","cabinet"
    ],

    "sports & fitness":[
        "cricket","football","bat",
        "ball","dumbbell","helmet",
        "glove","racket","skates"
    ],

    "automotive":[
        "car","bike","automotive",
        "seat cover","sun shade",
        "steering","horn"
    ],

    "beauty and personal care":[
        "shampoo","conditioner",
        "cream","face wash",
        "perfume","soap"
    ],

    "pens & stationery":[
        "notebook","diary",
        "pen","pencil","eraser",
        "folder","file"
    ],

    "home furnishing":[
        "curtain","bedsheet",
        "blanket","comforter",
        "pillow","towel"
    ],

    "home decor & festive needs":[
        "clock","painting",
        "plant","showpiece",
        "wall art"
    ]
}

# -----------------------------
# FIX CATEGORY
# -----------------------------

fixed = 0

for i, row in df.iterrows():

    category = str(row["category"]).strip().lower()

    if category in VALID_CATEGORIES:
        continue

    product = str(row["product_name"]).lower()

    product = str(row["product_name"]).lower()

    ptype = detect_product_type(product)

    CATEGORY_FROM_TYPE = {

        # Clothing
        "shirt": "Clothing",
        "tshirt": "Clothing",
        "kurta": "Clothing",
        "dress": "Clothing",
        "leggings": "Clothing",
        "jeans": "Clothing",
        "saree": "Clothing",
        "stole": "Clothing",
        "bra": "Clothing",
        "sock": "Clothing",

        # Footwear
        "shoe": "Footwear",
        "heel": "Footwear",
        "sandal": "Footwear",
        "flat": "Footwear",
        "boot": "Footwear",
        "loafer": "Footwear",

        # Bags
        "bag": "Bags, Wallets & Belts",
        "wallet": "Bags, Wallets & Belts",
        "clutch": "Bags, Wallets & Belts",
        "backpack": "Bags, Wallets & Belts",

        # Watches
        "watch": "Watches",

        # Furniture
        "chair": "Furniture",
        "table": "Furniture",
        "bed": "Furniture",
        "sofa": "Furniture",

        # Jewellery
        "ring": "Jewellery",
        "necklace": "Jewellery",
        "earring": "Jewellery",

        # Sunglasses
        "sunglasses": "Sunglasses",

        # Automotive
        "mirror": "Automotive",
        "helmet": "Automotive",

        # Home
        "floor mat": "Home Furnishing",
        "curtain": "Home Furnishing",
        "bedsheet": "Home Furnishing"
    }

    if ptype in CATEGORY_FROM_TYPE:
        df.at[i, "category"] = CATEGORY_FROM_TYPE[ptype]

        fixed += 1

print("Categories fixed :", fixed)
# -----------------------------
# NORMALIZE CATEGORY NAMES
# -----------------------------

df["category"] = (
    df["category"]
    .astype(str)
    .str.strip()
    .str.title()
)

# -----------------------------
# REMOVE REMAINING INVALID CATEGORIES
# -----------------------------

VALID_CATEGORIES = [
    "Clothing",
    "Footwear",
    "Jewellery",
    "Bags, Wallets & Belts",
    "Beauty And Personal Care",
    "Mobiles & Accessories",
    "Automotive",
    "Home Furnishing",
    "Home Decor & Festive Needs",
    "Furniture",
    "Sports & Fitness",
    "Watches",
    "Baby Care",
    "Kitchen & Dining",
    "Pens & Stationery",
    "Tools & Hardware",
    "Computers",
    "Cameras & Accessories",
    "Gaming",
    "Ebooks",
    "Pet Supplies",
    "Eyewear",
    "Sunglasses",
    "Toys & School Supplies",
    "Home Entertainment",
    "Health & Personal Care Appliances",
    "Home Improvement",
    "Home & Kitchen"
]

invalid = df[~df["category"].isin(VALID_CATEGORIES)]

print("\nRemaining Invalid Categories")
print(invalid["category"].value_counts())

# -----------------------------
# SAVE
# -----------------------------

df.to_csv(
    "products_cleaned.csv",
    index=False
)

print("\nSaved as products_cleaned.csv")

print("\nCATEGORY COUNTS")
print(df["category"].value_counts().head(40))