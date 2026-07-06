# recommendation/product_intelligence.py

import re

# =====================================================
# INNERWEAR PRODUCTS (REMOVE EVERYWHERE)
# =====================================================

INNERWEAR_KEYWORDS = {

    "bra",
    "bras",
    "lingerie",
    "brief",
    "briefs",
    "panty",
    "panties",
    "boxer",
    "boxers",
    "camisole",
    "slip",
    "petticoat",
    "nightwear",
    "innerwear",
    "shapewear",
    "thermal"
}

# =====================================================
# FASHION CATEGORIES
# =====================================================

FASHION_CATEGORIES = {

    "clothing",

    "footwear",

    "watches",

    "bags, wallets & belts",

    "jewellery",

    "eyewear",

    "sunglasses"

}

# =====================================================
# GENDER KEYWORDS
# =====================================================

GENDER_KEYWORDS = {

    "women":[
        "women",
        "woman",
        "ladies",
        "female"
    ],

    "men":[
        "men",
        "man",
        "male"
    ],

    "girls":[
        "girl",
        "girls"
    ],

    "boys":[
        "boy",
        "boys"
    ],

    "kids":[
        "kid",
        "kids",
        "children",
        "child"
    ],

    "unisex":[
        "unisex"
    ]
}


# =====================================================
# PRODUCT TYPE KEYWORDS
# =====================================================
PRODUCT_KEYWORDS = {

    # =====================================================
    # JEWELLERY
    # =====================================================

    "necklace": [
        "necklace", "chain", "choker"
    ],

    "ring": [
        "ring"
    ],

    "earring": [
        "earring", "earrings"
    ],

    "bracelet": [
        "bracelet", "bracelets"
    ],

    "bangle": [
        "bangle", "bangles"
    ],

    "pendant": [
        "pendant"
    ],

    # =====================================================
    # MEN'S / UNISEX TOPS
    # =====================================================

    "shirt": [

        "shirt",

        "formal shirt",

        "casual shirt",

        "checked shirt",

        "striped shirt",

        "printed shirt",

        "solid shirt",

        "slim fit shirt",

        "regular fit shirt"

    ],

    "tshirt": [
        "t-shirt",
        "tshirt",
        "tee",
        "round neck",
        "v-neck"
    ],

    "polo": [
        "polo"
    ],

    "hoodie": [
        "hoodie"
    ],

    "sweatshirt": [
        "sweatshirt"
    ],

    "sweater": [
        "sweater"
    ],

    "jacket": [
        "jacket",
        "windcheater",
        "wind cheater"
    ],

    "vest": [
        "vest"
    ],

    # =====================================================
    # WOMEN'S TOPS
    # =====================================================

    "top": [
        "top",
        "tops",
        "crop top",
        "tank top"
    ],

    "tunic": [
        "tunic"
    ],

    "blouse": [
        "blouse",
        "blouses"
    ],

    # =====================================================
    # BOTTOM WEAR
    # =====================================================

    "jeans": [
        "jeans"
    ],

    "trouser": [
        "trouser",
        "trousers",
        "pant",
        "pants"
    ],

    "trackpant": [
        "track pant",
        "track pants",
        "trackpant",
        "trackpants"
    ],

    "jogger": [
        "jogger",
        "joggers"
    ],

    "shorts": [
        "short",
        "shorts"
    ],

    "cargos": [
        "cargo",
        "cargos"
    ],

    "leggings": [
        "legging",
        "leggings"
    ],

    "jeggings": [
        "jegging",
        "jeggings"
    ],

    "palazzo": [
        "palazzo"
    ],

    "capri": [
        "capri",
        "capris"
    ],

    "skirt": [
        "skirt",
        "skirts"
    ],

    # =====================================================
    # ETHNIC WEAR
    # =====================================================

    "kurta": [

        "kurta",
        "kurti",

        "straight kurta",
        "printed kurta",
        "embroidered kurta",

        "ethnic kurta",

        "anarkali",
        "a-line kurta",

        "long kurti",
        "short kurti"

    ],

    "dress": [
        "dress",
        "gown"
    ],

    "dupatta": [
        "dupatta"
    ],

    "saree": [
        "saree"
    ],

    # =====================================================
    # FOOTWEAR
    # =====================================================

    "shoe": [
        "shoe",
        "shoes",
        "sneaker",
        "sneakers",
        "loafer",
        "loafers",
        "canvas shoes"
    ],

    "boot": [
        "boot",
        "boots"
    ],

    "sandal": [
        "sandal",
        "sandals",
        "heel",
        "heels",
        "slipper",
        "slippers",
        "clog",
        "clogs",
        "bellies",
        "wedges",
        "flat",
        "flats"
    ],

    # =====================================================
    # ACCESSORIES
    # =====================================================

    "watch":[

        "watch",

        "analog watch",

        "digital watch",

        "chronograph",

        "smart watch"

    ],

    "belt": [

        "belt",

        "leather belt",

        "formal belt",

        "casual belt"

    ],

    "backpack": [
        "backpack"
    ],

    "bag": [
        "bag",
        "bags",
        "handbag",
        "shoulder bag",
        "sling bag",
        "tote",
        "hobo",
        "satchel",
        "clutch",
        "pouch",
        "potli"
    ],

    "cap": [
        "cap",
        "caps",
        "hat"
    ],

    "scarf": [
        "scarf",
        "stole"
    ],

    "sock": [
        "sock",
        "socks"
    ],

    # =====================================================
    # FURNITURE
    # =====================================================

    "sofa": [
        "sofa",
        "sofa set",
        "sectional",
        "recliner",
        "loveseat",
        "couch"
    ],

    "chair": [
        "chair",
        "office chair",
        "dining chair",
        "study chair",
        "folding chair",
        "visitor chair",
        "arm chair"
    ],

    "table": [
        "table",
        "coffee table",
        "study table",
        "dining table",
        "side table",
        "computer table",
        "center table"
    ],

    "bed": [
        "bed",
        "cot",
        "bed frame",
        "bedframe"
    ],

    "wardrobe": [
        "wardrobe",
        "almirah",
        "closet"
    ],

    "cabinet": [
        "cabinet",
        "storage cabinet"
    ],

    "bookshelf": [
        "bookshelf",
        "book shelf",
        "bookcase"
    ],

    "tv_unit": [
        "tv unit",
        "tv stand",
        "entertainment unit"
    ],

    "desk": [
        "desk",
        "computer desk",
        "office desk"
    ],

    # =====================================================
    # HOME FURNISHING
    # =====================================================

    "bedsheet": [
        "bedsheet",
        "bed sheet",
        "sheet",
        "sheet set"
    ],

    "comforter": [
        "comforter",
        "comforters"
    ],

    "blanket": [
        "blanket",
        "blankets",
        "throw"
    ],

    "quilt": [
        "quilt",
        "quilts"
    ],

    "pillow": [
        "pillow",
        "pillows",
        "cushion",
        "cushions"
    ],

    "curtain": [
        "curtain",
        "curtains",
        "drape",
        "drapes"
    ],

    "carpet": [
        "carpet",
        "rug",
        "rugs",
        "floor mat"
    ],

    "mat": [
        "mat",
        "door mat",
        "bath mat",
        "yoga mat"
    ],

    "towel": [
        "towel",
        "towels",
        "bath towel",
        "hand towel"
    ],

    # =====================================================
    # ELECTRONICS
    # =====================================================

    "mobile": [
        "mobile",
        "smartphone",
        "phone",
        "iphone",
        "android"
    ],

    "tablet": [
        "tablet",
        "ipad"
    ],

    "laptop": [
        "laptop",
        "macbook"
    ],

    "desktop": [
        "desktop",
        "computer",
        "pc"
    ],

    "monitor": [
        "monitor",
        "display"
    ],

    "speaker": [
        "speaker",
        "bluetooth speaker",
        "soundbar"
    ],

    "headphone": [
        "headphone",
        "headphones",
        "earphone",
        "earphones",
        "earbuds",
        "buds"
    ],

    "watch_smart": [
        "smartwatch",
        "smart watch"
    ],

    "camera": [
        "camera",
        "dslr",
        "mirrorless",
        "camcorder"
    ],

    "printer": [
        "printer"
    ],

    "charger": [
        "charger",
        "adapter"
    ],

    "powerbank": [
        "power bank",
        "powerbank"
    ],

    "cable": [
        "usb cable",
        "charging cable",
        "hdmi cable",
        "cable"
    ],

    # =====================================================
    # KITCHEN & HOME APPLIANCES
    # =====================================================

    "mixer": [
        "mixer",
        "mixer grinder",
        "grinder"
    ],

    "cooker": [
        "pressure cooker",
        "cooker"
    ],

    "pan": [
        "pan",
        "frying pan",
        "kadai",
        "wok"
    ],

    "pot": [
        "pot",
        "saucepan"
    ],

    "knife": [
        "knife",
        "chef knife"
    ],

    "bottle": [
        "bottle",
        "water bottle"
    ],

    "flask": [
        "flask",
        "thermos"
    ],

    "lunchbox": [
        "lunch box",
        "lunchbox",
        "tiffin"
    ],

    "plate": [
        "plate",
        "plates"
    ],

    "cup": [
        "cup",
        "mug"
    ],

    "bowl": [
        "bowl",
        "bowls"
    ],

    # =====================================================
    # BEAUTY & PERSONAL CARE
    # =====================================================

    "perfume": [
        "perfume",
        "deodorant",
        "body spray"
    ],

    "shampoo": [
        "shampoo"
    ],

    "conditioner": [
        "conditioner"
    ],

    "soap": [
        "soap",
        "body wash"
    ],

    "facewash": [
        "face wash",
        "facewash"
    ],

    "cream": [
        "cream",
        "moisturizer",
        "moisturiser"
    ],

    "lotion": [
        "lotion"
    ],

    "lipstick": [
        "lipstick"
    ],

    "foundation": [
        "foundation"
    ],

    # =====================================================
    # SPORTS & FITNESS
    # =====================================================

    "cricket_bat": [
        "cricket bat",
    ],

    "football": [
        "football",
        "soccer ball"
    ],

    "basketball": [
        "basketball"
    ],

    "badminton": [
        "badminton racket",
        "badminton racquet",
        "racket"
    ],

    "tennis": [
        "tennis racket",
        "tennis racquet"
    ],

    "gym": [
        "dumbbell",
        "barbell",
        "gym",
        "weight",
        "kettlebell"
    ],

    "yoga": [
        "yoga mat",
        "yoga block"
    ],

    "helmet": [
        "helmet"
    ],

    "glove": [
        "glove",
        "gloves"
    ],

    "sports_bag": [
        "sports bag",
        "duffle bag",
        "duffel bag",
        "gym bag"
    ],

    # =====================================================
    # HOME DECOR
    # =====================================================

    "clock": [
        "wall clock",
        "clock"
    ],

    "lamp": [
        "lamp",
        "table lamp",
        "floor lamp"
    ],

    "mirror": [
        "mirror"
    ],

    "painting": [
        "painting",
        "wall art",
        "canvas painting"
    ],

    "vase": [
        "vase"
    ],

    "plant": [
        "artificial plant",
        "plant"
    ],

    "photo_frame": [
        "photo frame",
        "picture frame"
    ],

    "candle": [
        "candle"
    ],

    # =====================================================
    # AUTOMOTIVE
    # =====================================================

    "car_cover": [
        "car cover"
    ],

    "bike_cover": [
        "bike cover"
    ],

    "car_mat": [
        "car mat",
        "floor mat"
    ],

    "seat_cover": [
        "seat cover"
    ],

    "car_cleaner": [
        "car shampoo",
        "car cleaner",
        "polish"
    ],

    "helmet_bike": [
        "bike helmet",
        "motorcycle helmet"
    ],

    # =====================================================
    # STATIONERY
    # =====================================================

    "pen": [
        "pen"
    ],

    "pencil": [
        "pencil"
    ],

    "notebook": [
        "notebook",
        "diary"
    ],

    "folder": [
        "folder",
        "document folder"
    ],

    "calculator": [
        "calculator"
    ],

    "nighty": [
        "nighty"
    ],

    "kaftan": [
        "kaftan"
    ],

    "vanity_case": [
        "vanity case"
    ],

    "dumbbell": [
        "dumbbell"
    ],

    "clogs": [
        "clogs"
    ],

    "abaya": [
        "abaya"
    ],


    "jumpsuit": [
        "jumpsuit",
        "romper",
        "playsuit"
    ],

    "dungaree": [
        "dungaree",
        "overall"
    ],

    "waistcoat": [
        "waistcoat",
        "vest"
    ],

    "tie": [
        "tie",
        "neck tie"
    ],

    "blazer": [
        "blazer"
    ],

    "coat": [
        "coat"
    ],

    "cardigan": [
        "cardigan"
    ],

    "shrug": [
        "shrug"
    ],

    "poncho": [
        "poncho"
    ],

    "stole": [
        "stole"
    ],

    "wallet": [
        "wallet"
    ],

    "sling_bag": [
        "sling bag"
    ],

    "handbag": [
        "handbag",
        "hand bag"
    ],

    "clutch": [
        "clutch"
    ],

    "duffle_bag": [
        "duffle",
        "duffel"
    ],

    "trolley_bag": [
        "trolley bag"
    ],

    "travel_bag": [
        "travel bag"
    ],

    "tripod": [
        "tripod"
    ],

    "keyboard": [
        "keyboard"
    ],

    "mouse": [
        "mouse"
    ],

    "pendrive": [
        "pen drive",
        "pendrive",
        "usb"
    ],

    "hard_disk": [
        "hard disk",
        "external hard disk"
    ],

    "mattress": [
        "mattress"
    ],

    "cushion": [
        "cushion"
    ],


    "bedspread": [
        "bedspread"
    ],

    "moisturizer": [
        "moisturizer"
    ],


    "mascara": [
        "mascara"
    ],

    "eyeliner": [
        "eyeliner"
    ],

    "anklet": [
        "anklet"
    ],

    "brooch": [
        "brooch"
    ]

}


# =====================================================
# PRODUCT COMPATIBILITY
# =====================================================
COMPATIBILITY_MAP = {

    # =====================================================
    # JEWELLERY
    # =====================================================

    "necklace": [
        "earring",
        "ring",
        "bracelet",
        "bangle",
        "pendant"
    ],

    "ring": [
        "necklace",
        "earring",
        "bracelet",
        "bangle"
    ],

    "earring": [
        "necklace",
        "ring",
        "bracelet",
        "bangle"
    ],

    "bracelet": [
        "ring",
        "earring",
        "watch"
    ],

    "bangle": [
        "ring",
        "earring",
        "necklace"
    ],

    # =====================================================
    # MEN'S TOPS
    # =====================================================

    "shirt": [
        "jeans",
        "trouser",
        "belt",
        "watch",
        "shoe",
        "wallet"
    ],

    "tshirt": [
        "jeans",
        "shorts",
        "shoe",
        "watch",
        "backpack"
    ],

    "polo": [
        "jeans",
        "shoe",
        "watch"
    ],

    "hoodie": [
        "jeans",
        "shoe",
        "backpack"
    ],

    "sweatshirt": [
        "jeans",
        "shoe",
        "watch"
    ],

    "sweater": [
        "jeans",
        "shoe",
        "watch"
    ],

    "cardigan": [
        "jeans",
        "trouser",
        "watch",
        "shoe"
    ],

    "jacket": [
        "jeans",
        "shoe",
        "watch"
    ],

    "blazer": [
        "trouser",
        "belt",
        "watch",
        "shoe"
    ],

    "waistcoat": [
        "shirt",
        "trouser",
        "watch"
    ],

    "vest": [
        "jeans",
        "shoe"
    ],

    # =====================================================
    # WOMEN'S TOPS
    # =====================================================

    "top": [
        "jeans",
        "leggings",
        "jeggings",
        "skirt",
        "palazzo"
    ],

    "tunic": [
        "leggings",
        "jeggings",
        "palazzo"
    ],

    "blouse": [
        "skirt",
        "saree",
        "palazzo"
    ],

    # =====================================================
    # BOTTOM WEAR
    # =====================================================

    "jeans": [
        "shirt",
        "tshirt",
        "hoodie",
        "cardigan",
        "belt",
        "shoe",
        "watch"
    ],

    "trouser": [
        "shirt",
        "belt",
        "watch",
        "shoe"
    ],

    "trackpant": [
        "tshirt",
        "shoe",
        "cap"
    ],

    "jogger": [
        "tshirt",
        "shoe"
    ],

    "shorts": [
        "tshirt",
        "shoe",
        "cap"
    ],

    "cargos": [
        "tshirt",
        "shoe",
        "belt"
    ],

    "leggings": [
        "kurta",
        "tunic",
        "top",
        "dupatta"
    ],

    "jeggings": [
        "top",
        "tunic",
        "kurta"
    ],

    "palazzo": [
        "kurta",
        "top",
        "dupatta"
    ],

    "skirt": [
        "top",
        "blouse"
    ],

    # =====================================================
    # ETHNIC WEAR
    # =====================================================

    "kurta": [
        "leggings",
        "palazzo",
        "dupatta",
        "earring",
        "necklace",
        "sandal",
        "bag"
    ],


    "abaya": [
        "hijab",
        "scarf",
        "sandal",
        "handbag"
    ],

    "dress": [
        "sandal",
        "heel",
        "handbag",
        "bag",
        "necklace",
        "earring",
        "bracelet"
    ],

    "saree": [
        "blouse",
        "necklace",
        "earring",
        "bangle",
        "sandal",
        "bag"
    ],

    # =====================================================
    # FOOTWEAR
    # =====================================================

    "shoe": [
        "jeans",
        "shirt",
        "watch",
        "belt",
        "wallet"
    ],

    "boot": [
        "jeans",
        "jacket"
    ],

    "sandal": [
        "dress",
        "kurta",
        "bag",
        "leggings"
    ],

    # =====================================================
    # ACCESSORIES
    # =====================================================

    "watch": [
        "shirt",
        "tshirt",
        "belt",
        "shoe",
        "wallet",
        "sunglasses",
        "bracelet"
    ],

    "belt": [
        "shirt",
        "jeans",
        "trouser",
        "watch",
        "shoe"
    ],

    "wallet": [
        "belt",
        "watch",
        "shirt"
    ],

    "backpack": [
        "tshirt",
        "hoodie",
        "shoe"
    ],

    "bag": [
        "dress",
        "kurta",
        "top",
        "sandal",
        "watch"
    ],

    # =====================================================
    # FURNITURE
    # =====================================================

    "sofa": [
        "table",
        "carpet",
        "cushion"
    ],

    "chair": [
        "table"
    ],

    "table": [
        "chair"
    ],

    "bed": [
        "bedsheet",
        "comforter",
        "blanket",
        "pillow"
    ],

    "wardrobe": [],

    "cabinet": [],

    "bookshelf": [],

    "tv_unit": [],

    "desk": [
        "chair"
    ],

    # =====================================================
    # HOME FURNISHING
    # =====================================================

    "bedsheet": [
        "comforter",
        "blanket",
        "pillow"
    ],

    "comforter": [
        "bedsheet",
        "pillow"
    ],

    "blanket": [
        "bedsheet",
        "comforter"
    ],

    "quilt": [
        "bedsheet",
        "pillow"
    ],

    "pillow": [
        "bedsheet",
        "comforter"
    ],

    "curtain": [
        "carpet"
    ],

    "carpet": [
        "sofa",
        "table"
    ],

    "mat": [],

    "towel": [],

    # =====================================================
    # ELECTRONICS
    # =====================================================

    "mobile": [
        "charger",
        "cable",
        "headphone",
        "powerbank"
    ],

    "tablet": [
        "charger",
        "headphone"
    ],

    "laptop": [
        "mouse",
        "keyboard",
        "speaker"
    ],

    "desktop": [
        "monitor",
        "keyboard",
        "mouse",
        "speaker"
    ],

    "monitor": [
        "keyboard",
        "mouse"
    ],

    "keyboard": [
        "mouse"
    ],

    "mouse": [
        "keyboard"
    ],

    "speaker": [
        "headphone"
    ],

    "headphone": [
        "mobile",
        "laptop"
    ],

    "watch_smart": [
        "headphone"
    ],

    "camera": [],

    "printer": [],

    "charger": [
        "cable"
    ],

    "powerbank": [
        "charger"
    ],

    "cable": [
        "charger"
    ],

    # =====================================================
    # KITCHEN
    # =====================================================

    "mixer": [],

    "cooker": [
        "pan",
        "pot"
    ],

    "pan": [
        "pot"
    ],

    "pot": [
        "pan"
    ],

    "knife": [
        "plate"
    ],

    "bottle": [
        "lunchbox"
    ],

    "flask": [
        "cup"
    ],

    "lunchbox": [
        "bottle"
    ],

    "plate": [
        "bowl"
    ],

    "cup": [
        "flask"
    ],

    "bowl": [
        "plate"
    ],

    # =====================================================
    # BEAUTY
    # =====================================================

    "perfume": [
        "lotion"
    ],

    "shampoo": [
        "conditioner"
    ],

    "conditioner": [
        "shampoo"
    ],

    "soap": [
        "lotion"
    ],

    "facewash": [
        "cream"
    ],

    "cream": [
        "facewash"
    ],

    "lotion": [
        "perfume"
    ],

    "lipstick": [
        "foundation"
    ],

    "foundation": [
        "lipstick"
    ],

    # =====================================================
    # SPORTS
    # =====================================================

    "cricket_bat": [
        "glove"
    ],

    "football": [],

    "basketball": [],

    "badminton": [
        "sports_bag"
    ],

    "tennis": [
        "sports_bag"
    ],

    "gym": [
        "sports_bag"
    ],

    "yoga": [],

    "helmet": [],

    "glove": [
        "cricket_bat"
    ],

    "sports_bag": [
        "gym"
    ],
    # =====================================================
    # HOME DECOR
    # =====================================================

    "clock": [],

    "lamp": [
        "table"
    ],

    "mirror": [],

    "painting": [],

    "vase": [
        "table"
    ],

    "plant": [
        "vase"
    ],

    "photo_frame": [],

    "candle": [],

    # =====================================================
    # AUTOMOTIVE
    # =====================================================

    "car_cover": [],

    "bike_cover": [],

    "car_mat": [
        "seat_cover"
    ],

    "seat_cover": [
        "car_mat"
    ],

    "car_cleaner": [],

    "helmet_bike": [],

    # =====================================================
    # STATIONERY
    # =====================================================

    "pen": [
        "notebook"
    ],

    "pencil": [
        "notebook"
    ],

    "notebook": [
        "pen"
    ],

    "folder": [],

    "calculator": [],

    "jumpsuit": [
        "heel",
        "sandal",
        "bag",
        "watch",
        "bracelet"
    ],

    "nighty": [
        "slipper"
    ],

    "shrug": [
        "dress",
        "top",
        "tshirt"
    ],

    "dumbbell": [
        "bottle"
    ]
}

# =====================================================
# CANONICAL CATEGORY MAP
# =====================================================

TYPE_TO_CATEGORY = {

    # Clothing
    "shirt": "Clothing",
    "tshirt": "Clothing",
    "kurta": "Clothing",
    "dress": "Clothing",
    "top": "Clothing",
    "jeans": "Clothing",
    "leggings": "Clothing",
    "saree": "Clothing",
    "lehenga": "Clothing",
    "dupatta": "Clothing",
    "blazer": "Clothing",
    "hoodie": "Clothing",
    "jacket": "Clothing",
    "sweater": "Clothing",
    "bra": "Clothing",
    "brief": "Clothing",
    "panty": "Clothing",
    "sock": "Clothing",
    "jumpsuit": "Clothing",
    "nighty": "Clothing",
    "shrug": "Clothing",
    "kaftan": "Clothing",
    "dungaree": "Clothing",
    "waistcoat": "Clothing",

    "clogs": "Footwear",

    "vanity_case": "Beauty And Personal Care",

    "bottle": "Kitchen & Dining",

    # Footwear
    "shoe": "Footwear",
    "sandal": "Footwear",
    "heel": "Footwear",
    "flat": "Footwear",
    "boot": "Footwear",
    "loafer": "Footwear",
    "slipper": "Footwear",

    # Jewellery
    "ring": "Jewellery",
    "necklace": "Jewellery",
    "earring": "Jewellery",
    "bracelet": "Jewellery",
    "bangle": "Jewellery",
    "pendant": "Jewellery",

    # Bags
    "bag": "Bags, Wallets & Belts",
    "wallet": "Bags, Wallets & Belts",
    "backpack": "Bags, Wallets & Belts",
    "clutch": "Bags, Wallets & Belts",

    # Watches
    "watch": "Watches",

    # Furniture
    "chair": "Furniture",
    "table": "Furniture",
    "bed": "Furniture",
    "sofa": "Furniture",
    "wardrobe": "Furniture",

    # Home Furnishing
    "curtain": "Home Furnishing",
    "bedsheet": "Home Furnishing",
    "blanket": "Home Furnishing",
    "pillow": "Home Furnishing",
    "floor_mat": "Home Furnishing",

    # Home Decor
    "painting": "Home Decor & Festive Needs",
    "clock": "Home Decor & Festive Needs",
    "plant": "Home Decor & Festive Needs",
    "showpiece": "Home Decor & Festive Needs",

    # Beauty
    "perfume": "Beauty And Personal Care",
    "cream": "Beauty And Personal Care",
    "shampoo": "Beauty And Personal Care",
    "conditioner": "Beauty And Personal Care",

    # Sports
    "cricket_bat": "Sports & Fitness",
    "football": "Sports & Fitness",
    "dumbbell": "Sports & Fitness",
    "helmet": "Sports & Fitness",
    "glove": "Sports & Fitness",

    # Automotive
    "car_accessory": "Automotive",

    # Electronics
    "mobile": "Mobiles & Accessories",
    "charger": "Mobiles & Accessories",
    "headphone": "Mobiles & Accessories",
    "earphone": "Mobiles & Accessories",

    # Stationery
    "notebook": "Pens & Stationery",
    "pen": "Pens & Stationery",
    "folder": "Pens & Stationery"
}


def get_canonical_category(product_type, original_category):

    product_type = str(product_type).lower().strip()

    if product_type in TYPE_TO_CATEGORY:
        return TYPE_TO_CATEGORY[product_type]

    category = str(original_category).strip()

    if category != "":
        return category.title()

    return "Others"

# =====================================================
# HELPERS
# =====================================================

def normalize(text):

    if text is None:
        return ""

    text = str(text).lower()

    words = []

    for w in text.split():

        if w not in words:

            words.append(w)

    return " ".join(words)

def tokenize(text):

    text = normalize(text)

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    return text.split()

def detect_gender(product):

    text = normalize(product)

    # -------------------------
    # WOMEN
    # -------------------------

    if re.search(
        r"\bwomen\b|\bwoman\b|\bwomen's\b|\bladies\b|\bfemale\b",
        text,
        flags=re.IGNORECASE
    ):
        return "women"

    # -------------------------
    # MEN
    # -------------------------

    if re.search(
        r"\bmen\b|\bman\b|\bmen's\b|\bmale\b",
        text,
        flags=re.IGNORECASE
    ):
        return "men"

    # -------------------------
    # BOYS
    # -------------------------

    if re.search(
        r"\bboys?\b",
        text,
        flags=re.IGNORECASE
    ):
        return "boys"

    # -------------------------
    # GIRLS
    # -------------------------

    if re.search(
        r"\bgirls?\b",
        text,
        flags=re.IGNORECASE
    ):
        return "girls"

    # -------------------------
    # KIDS
    # -------------------------

    if re.search(
        r"\bkids?\b|\bchildren\b|\bchild\b",
        text,
        flags=re.IGNORECASE
    ):
        return "kids"

    # -------------------------
    # UNISEX
    # -------------------------

    if re.search(
        r"\bunisex\b",
        text,
        flags=re.IGNORECASE
    ):
        return "unisex"

    return ""



def detect_product_type(text):

    words = tokenize(text)

    if not words:
        return "other"

    candidates = set(words)

    # 2-word phrases
    for i in range(len(words) - 1):
        candidates.add(
            words[i] + " " + words[i + 1]
        )

    # 3-word phrases
    for i in range(len(words) - 2):
        candidates.add(
            words[i]
            + " "
            + words[i + 1]
            + " "
            + words[i + 2]
        )

    best_type = "other"
    best_score = 0

    text = normalize_text(text)

    if text == "":
        return "other"

    for product_type, keywords in PRODUCT_KEYWORDS.items():

        for keyword in keywords:

            if keyword in candidates:

                score = (
                        len(keyword.split()) * 100
                        + len(keyword)
                )

                if score > best_score:
                    best_score = score
                    best_type = product_type

    return best_type

def get_compatible_types(product_type):

    product_type = normalize(product_type)

    return COMPATIBILITY_MAP.get(product_type, [])


def is_innerwear(name):

    name = normalize(name)

    return any(

        word in name

        for word in INNERWEAR_KEYWORDS

    )


def is_fashion(category):

    return normalize(category) in FASHION_CATEGORIES


# =====================================================
# FILTER RECOMMENDATION CANDIDATES
# =====================================================

def filter_compatible_products(
        df,
        selected_product
):

    if df.empty:
        return df

    df = df.copy()

    # ----------------------------------------
    # SELECTED PRODUCT DETAILS
    # ----------------------------------------

    selected_name = normalize(
        selected_product["product_name"]
    )

    selected_gender = detect_gender(
        selected_name
    )

    # ----------------------------------------
    # REMOVE INNERWEAR
    # ----------------------------------------

    df = df[
        ~df["product_name"]
        .apply(is_innerwear)
    ]

    # ----------------------------------------
    # REMOVE CURRENT PRODUCT
    # ----------------------------------------

    df = df[
        df["product_id"]
        != selected_product["product_id"]
    ]

    # ----------------------------------------
    # DETECT PRODUCT GENDER
    # ----------------------------------------

    df["detected_gender"] = df[
        "product_name"
    ].apply(detect_gender)

    # ----------------------------------------
    # GENDER FILTER
    # ----------------------------------------

    if selected_gender != "":

        df = df[

            (df["detected_gender"] == selected_gender)

            |

            (df["detected_gender"] == "")

            |

            (df["detected_gender"] == "unisex")

        ]

    # ----------------------------------------
    # REMOVE DUPLICATES
    # ----------------------------------------

    df = df.drop_duplicates(
        subset="product_name"
    )

    return df.reset_index(drop=True)

# =====================================================
# FEATURE BUILDERS
# =====================================================

def build_combined_features(product):

    category = normalize(
        product.get("category", "")
    )

    product_name = normalize(
        product.get("product_name", "")
    )

    # Use already computed features if available
    gender = normalize(
        product.get("gender_feature", "")
    )

    product_type = normalize(
        product.get("type_feature", "")
    )

    return " ".join([

        category,
        category,

        gender,
        gender,
        gender,

        product_type,
        product_type,
        product_type,

        product_name

    ])


def common_word_score(text1, text2):

    words1 = set(
        normalize(text1).split()
    )

    words2 = set(
        normalize(text2).split()
    )

    return len(words1 & words2)


def same_brand_score(name1, name2):

    brand1 = normalize(name1).split()

    brand2 = normalize(name2).split()

    if not brand1 or not brand2:

        return 0

    return 10 if brand1[0] == brand2[0] else 0


def normalize_text(text):
    """
    Safely normalize text for comparisons.
    """

    if text is None:
        return ""

    return " ".join(
        str(text)
        .lower()
        .strip()
        .split()
    )

# =====================================================
# PRE-NORMALIZE PRODUCT KEYWORDS (RUN ONCE)
# =====================================================

PRODUCT_KEYWORDS = {
    product_type: [
        normalize(keyword)
        for keyword in keywords
    ]
    for product_type, keywords in PRODUCT_KEYWORDS.items()
}