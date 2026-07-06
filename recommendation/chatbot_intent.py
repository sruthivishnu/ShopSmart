import re


def extract_chatbot_intent(query):

    query = query.lower()

    intent = {

        "category": None,
        "type": None,
        "gender": None,
        "occasion": None,
        "budget": None

    }

    # ------------------
    # GENDER
    # ------------------

    if re.search(
            r'\b(women|woman|ladies|girl|girls)\b',
            query
    ):

        intent["gender"] = "women"

    elif re.search(
            r'\b(men|man|boys|boy)\b',
            query
    ):

        intent["gender"] = "men"

    elif re.search(
            r'\b(kid|kids|child|children)\b',
            query
    ):

        intent["gender"] = "kids"

    # ------------------
    # CATEGORY
    # ------------------

    category_map = {

        "footwear": "footwear",
        "shoe": "footwear",
        "shoes": "footwear",
        "sneaker": "footwear",
        "sneakers": "footwear",
        "sandal": "footwear",
        "sandals": "footwear",
        "heel": "footwear",
        "heels": "footwear",
        "running": "footwear",
        "sports shoe": "footwear",

        "watch": "watches",
        "watches": "watches",

        "sling bag": "bags",
        "sling": "bags",

        "shoulder bag": "bags",
        "shoulder": "bags",

        "laptop bag": "bags",

        "backpack": "bags",
        "backpacks": "bags",

        "tote": "bags",
        "handbag": "bags",

        "bag": "bags",
        "bags": "bags",

        "accessory": "bags",
        "accessories": "bags",

        "kurta": "clothing",
        "kurti": "clothing",
        "kurtis": "clothing",
        "kurtas": "clothing",

        "shirt": "clothing",
        "dress": "clothing",
        "jeans": "clothing",

        "clothes": "clothing",
        "clothing": "clothing",

        "outfit": "clothing",
        "outfits": "clothing",

        "apparel": "clothing",

        "perfume": "beauty",
        "lipstick": "beauty",


        "pants": "clothing",
        "trouser": "clothing",
        "trousers": "clothing",

        "top": "clothing",
        "tops": "clothing",

        "necklace": "jewellery",
        "necklaces": "jewellery",

        "shampoo": "beauty",

        "furniture": "furniture",
        "sofa": "furniture",
        "chair": "furniture",
        "table": "furniture",

        "wallet": "bags",
        "wallets": "bags",

        "belt": "bags",
        "belts": "bags",

        "handbag": "bags",
        "handbags": "bags"
    }

    for key, value in category_map.items():

        if re.search(rf'\b{re.escape(key)}\b', query):

            intent["category"] = value

            # normalize bag types
            if key in ["sling", "sling bag"]:
                intent["type"] = "sling"

            elif key in ["shoulder", "shoulder bag"]:
                intent["type"] = "shoulder"

            elif key in ["backpack", "backpacks"]:
                intent["type"] = "backpack"

            elif key == "laptop bag":
                intent["type"] = "laptop"

            else:

                if key not in [
                    "clothes",
                    "clothing",
                    "outfit",
                    "outfits",
                    "apparel"
                ]:
                    intent["type"] = key

            break

    # Special handling for shampoo

    # ---------------------------------
    # TYPE NORMALIZATION
    # ---------------------------------

    type_normalization = {

        # Footwear
        "shoes": "shoe",
        "sneakers": "sneaker",
        "sandals": "sandal",
        "heels": "heel",

        # Clothing
        "kurtis": "kurta",
        "kurtas": "kurta",
        "shirts": "shirt",
        "dresses": "dress",
        "tops": "top",
        "trousers": "trouser",
        "pants": "pant",

        # Bags
        "bags": "bag",
        "handbags": "handbag",
        "wallets": "wallet",
        "belts": "belt",
        "backpacks": "backpack",

        # Watches
        "watches": "watch",

        # Jewellery
        "necklaces": "necklace"

    }

    if intent["type"] in type_normalization:
        intent["type"] = type_normalization[
            intent["type"]
        ]

    # ---------------------------------
    # SPECIAL PRODUCTS
    # ---------------------------------

    if "shampoo" in query:
        intent["category"] = "beauty"
        intent["type"] = "shampoo"

    # ------------------
    # OCCASION
    # ------------------

    occasion_words = [

        "college",
        "office",
        "party",
        "casual",
        "daily",
        "running",
        "sports"

    ]

    for word in occasion_words:

        if word in query:

            intent["occasion"] = word

            break

    # Office-related natural language

    if "work" in query:

        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "professional" in query:

        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "meeting" in query:

        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "meetings" in query:

        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "interview" in query:
        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "formal" in query:
        intent["occasion"] = "office"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "clothes" in query:

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "outfit" in query:

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "outfits" in query:

        if intent["category"] is None:
            intent["category"] = "clothing"

    # ------------------
    # INTERVIEW
    # ------------------

    if "interview" in query:

        intent["occasion"] = "interview"

        if intent["category"] is None:
            intent["category"] = "clothing"

    # ------------------
    # TRAVEL / VACATION
    # ------------------

    if (
            "travel" in query
            or "trip" in query
            or "vacation" in query
            or "holiday" in query
    ):

        intent["occasion"] = "travel"

        if intent["category"] is None:
            intent["category"] = "clothing"

    # ------------------
    # PARTY
    # ------------------

    if "party" in query:

        intent["occasion"] = "party"

        if intent["category"] is None:
            intent["category"] = "clothing"

    # ------------------
    # GIFT
    # ------------------

    if "gift" in query:
        intent["occasion"] = "gift"

    # ------------------
    # NATURAL LANGUAGE PHRASES
    # ------------------

    # ------------------
    # SMART SHOPPING PHRASES
    # ------------------

    # Laptop / Office Bags
    if (
            "laptop" in query
            or "office bag" in query
            or "carry my laptop" in query
    ):
        intent["category"] = "bags"
        intent["type"] = "laptop"

    # College
    if (
            "college" in query
            or "campus" in query
            or "joining college" in query
    ):
        if intent["category"] is None:
            intent["category"] = "bags"

        if intent["type"] is None:
            intent["type"] = "backpack"

        intent["occasion"] = "college"

    # Walking
    if (
            "walking" in query
            or "long walk" in query
            or "walk" in query
    ):
        intent["category"] = "footwear"

        if intent["type"] is None:
            intent["type"] = "shoes"

        intent["occasion"] = "walking"

    # Trekking / Hiking
    if (
            "trek" in query
            or "trekking" in query
            or "hiking" in query
    ):
        intent["category"] = "footwear"
        intent["type"] = "sports shoes"
        intent["occasion"] = "trekking"

    # Gym
    if (
            "gym" in query
            or "workout" in query
            or "fitness" in query
    ):
        intent["category"] = "sports"
        intent["occasion"] = "gym"

    # Rain
    if (
            "rain" in query
            or "rainy" in query
            or "monsoon" in query
    ):
        if intent["category"] is None:
            intent["category"] = "footwear"

        if intent["type"] is None:
            intent["type"] = "sandals"

        intent["occasion"] = "rain"

    # Beach / Vacation
    if (
            "beach" in query
            or "goa" in query
            or "vacation" in query
            or "holiday" in query
    ):
        if intent["category"] is None:
            intent["category"] = "clothing"

        intent["occasion"] = "travel"

    if "goa" in query:

        intent["occasion"] = "travel"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if "birthday" in query:
        intent["occasion"] = "gift"

    if "engagement" in query:

        intent["occasion"] = "party"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if any(
            word in query
            for word in [
                "sister",
                "mother",
                "mom",
                "mum",
                "wife",
                "girlfriend",
                "daughter",
                "aunt"
            ]
    ):
        intent["gender"] = "women"

    if any(
            word in query
            for word in [
                "brother",
                "father",
                "dad",
                "husband",
                "boyfriend",
                "son",
                "uncle"
            ]
    ):
        intent["gender"] = "men"

    if (
            "next week" in query
            and
            "interview" in query
    ):

        intent["occasion"] = "interview"

        if intent["category"] is None:
            intent["category"] = "clothing"

    if (
            "comfortable" in query
            and
            (
                    "walking" in query
                    or
                    "walk" in query
            )
    ):
        intent["occasion"] = "daily"
        intent["category"] = "footwear"

    # ------------------
    # PRICE LANGUAGE
    # ------------------

    if any(
            word in query
            for word in [
                "cheap",
                "budget",
                "affordable",
                "low cost",
                "low-cost"
            ]
    ):

        if intent["budget"] is None:
            intent["budget"] = 1000

    if "premium" in query:

        if intent["budget"] is None:
            intent["budget"] = 5000

    if "luxury" in query:

        if intent["budget"] is None:
            intent["budget"] = 10000

    # ------------------
    # STYLE MATCH
    # ------------------

    if (
            "goes with" in query
            or "matches with" in query
            or "match with" in query
            or "what matches" in query
            or "wear with" in query
    ):
        intent["occasion"] = "style_match"

    # ------------------
    # BUDGET
    # ------------------

    match = re.search(
        r'under\s*(\d+)',
        query
    )

    if match:

        intent["budget"] = int(
            match.group(1)
        )

    print("EXTRACTED INTENT =", intent)

    return intent