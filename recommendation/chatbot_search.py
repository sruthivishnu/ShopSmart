from recommendation.model import products_df
import pandas as pd
occasion_map = {

    "college": [
        "backpack",
        "canvas",
        "casual",
        "shoulder bag",
        "sling bag"
    ],


    "office": [
        "formal",
        "loafer",
        "heel",
        "sandal",
        "shoe",
        "blazer",
        "shirt",
        "trouser",
        "waistcoat",

    ],



    "party": [
        "dress",
        "party",
        "watch",
        "heels",
        "fashion"
    ],

    "running": [
        "sports shoe"
    ],

    "sports": [
        "sports shoe"
    ],

    "interview": [
        "formal",
        "shirt",
        "waistcoat"
    ],

    "travel": [
        "casual",
        "shirt",
        "jeans",
        "backpack",
        "canvas",
        "sneaker"
    ],

    "party": [
        "dress",
        "party",
        "watch",
        "heels",
        "fashion"
    ],

    "gift": [
        "watch",
        "bag",
        "wallet",
        "perfume",
        "jewellery"
    ]

}

def chatbot_search(intent):
    print("INTENT =", intent)
    print("CHATBOT SEARCH EXECUTED")

    results = products_df.copy()

    results = results[

        results['image'].notna()

        &

        (~results['image']
         .str.contains(
            'default.jpg',
            case=False,
            na=False
        ))

        ]
    print("AFTER IMAGE FILTER =", len(results))

    # STYLE MATCH USING FBT CATEGORY LOGIC

    if intent["occasion"] == "style_match":

        style_match_map = {

            "heel": {
                "categories": "clothing|jewellery|bags",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "bag": r'handbag|sling|shoulder|bag',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "heels": {
                "categories": "clothing|jewellery|bags",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "bag": r'handbag|sling|shoulder|bag',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "bag": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker|wedge',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "bags": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker|wedge',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "handbag": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "shoulder": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "jeans": {
                "categories": "clothing|footwear|bags|watches",

                "groups": {

                    "top": r'top',

                    "shirt": r'shirt|t-shirt|tee',

                    "footwear": r'sneaker|shoe|canvas|casual shoe',

                    "bag": r'handbag|sling|backpack',

                    "watch": r'watch'
                }
            },

            "kurti": {
                "categories": "clothing|footwear|bags|jewellery",
                "groups": {
                    "leggings": r'legging',
                    "footwear": r'sandal|heel|wedge',
                    "bag": r'handbag|sling',
                    "jewellery": r'necklace|earring|bracelet|ring',
                    "dupatta": r'dupatta'
                }
            },

            "sling": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "backpack": {
                "categories": "clothing|footwear|jewellery",
                "groups": {
                    "dress": r'dress',
                    "kurti": r'kurti|kurta',
                    "top": r'top|shirt',
                    "footwear": r'sandal|heel|shoe|sneaker',
                    "jewellery": r'necklace|earring|bracelet|ring'
                }
            },

            "kurta": {
                "categories": "clothing|footwear|bags|jewellery",
                "groups": {
                    "leggings": r'legging',
                    "footwear": r'sandal|heel|wedge',
                    "bag": r'handbag|sling',
                    "jewellery": r'necklace|earring|bracelet|ring',
                    "dupatta": r'dupatta'
                }
            }
        }

        if intent["type"] in style_match_map:
            results = products_df[

                products_df["category"]
                .fillna("")
                .str.contains(
                    style_match_map[
                        intent["type"]
                    ]["categories"],
                    case=False,
                    na=False,
                    regex=True
                )

            ]

            results = results[

                ~

                results["product_name"]
                .fillna("")
                .str.contains(
                    r'bra|lingerie|innerwear|nipple|stick-on',
                    case=False,
                    na=False,
                    regex=True
                )

            ]

            results["style_score"] = 0

            results.loc[
                results["product_name"]
                .str.contains(
                    r'dress|gown',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 100

            results.loc[
                results["product_name"]
                .str.contains(
                    r'kurti|kurta',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 90

            results.loc[
                results["product_name"]
                .str.contains(
                    r'handbag|shoulder bag|sling',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 80

            results.loc[
                results["product_name"]
                .str.contains(
                    r'necklace|earring|bracelet|jewellery',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 70

            results.loc[
                results["product_name"]
                .str.contains(
                    r'top',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 60

            results.loc[
                results["product_name"]
                .str.contains(
                    r'shirt',
                    case=False,
                    na=False,
                    regex=True
                ),
                "style_score"
            ] = 50

            results = results[

                results["gender_feature"]
                .fillna("")
                .str.contains(
                    "women",
                    case=False,
                    na=False
                )

            ]

            results = results[

                ~

                results["gender_feature"]
                .fillna("")
                .str.contains(
                    r'kids|girls|boys',
                    case=False,
                    na=False,
                    regex=True
                )

            ]

            print("STYLE MATCH RESULTS =", len(results))

            if intent["type"] in ["heel", "heels"]:
                results = results[
                    results["product_name"]
                    .str.contains(
                        r'dress|kurti|kurta|top|shirt|handbag|sling|shoulder|necklace|earring|bracelet',
                        case=False,
                        na=False,
                        regex=True
                    )
                ]

            results = results[results["style_score"] > 0]

            results = (

                results

                .sort_values(
                    by=["style_score", "rating"],
                    ascending=False
                )

                .drop_duplicates(
                    subset="product_name"
                )

            )

            final_results = []

            for group_name, pattern in (

                    style_match_map[
                        intent["type"]
                    ]["groups"].items()

            ):
                match = results[
                    results["product_name"]
                    .str.contains(
                        pattern,
                        case=False,
                        na=False,
                        regex=True
                    )
                ].head(1)

                if not match.empty:
                    final_results.append(match)

            results = pd.concat(final_results)

            return results


    if not intent["category"]:

        if intent.get("occasion") != "gift":
            return results.iloc[0:0]

    # CATEGORY

    if intent["category"]:

        results = results[

            results["category"]
            .fillna('')
            .str.contains(
                intent["category"],
                case=False,
                na=False
            )

        ]
        print("AFTER CATEGORY =", len(results))

    # WEDDING OCCASION

    if intent["occasion"] == "wedding":
        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'kurta|anarkali|lehenga|saree|sherwani|ethnic',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER WEDDING FILTER =", len(results))

    # GENDER

    if intent["gender"]:

        results = results[

            results["gender_feature"]
            .fillna('')
            .str.contains(
                rf'\b{intent["gender"]}\b',
                case=False,
                na=False,
                regex=True
            )

        ]
        print("AFTER GENDER =", len(results))

        print(
            results["gender_feature"]
            .value_counts()
            .head(10)
        )

        print("AFTER GENDER SAMPLE")
        print(
            results[
                ["product_name", "gender_feature"]
            ].head(20)
        )

        if intent["type"] == "jeans":
            print(
                results[
                    ["product_name", "type_feature"]
                ]
                .head(30)
                .to_string()
            )
            print(
                results[
                    results["product_name"]
                    .str.contains(
                        "Mast",
                        case=False,
                        na=False
                    )
                ][
                    ["product_name", "gender_feature"]
                ]
            )

    # EXTRA WATCH FILTER

    if intent["category"] == "watches":

        if intent["gender"] == "men":

            results = results[

                results["product_name"]
                .fillna('')
                .str.contains(
                    r'for men|men|boys',
                    case=False,
                    na=False,
                    regex=True
                )

                &

                ~

                results["product_name"]
                .fillna('')
                .str.contains(
                    r'for women|women|girls',
                    case=False,
                    na=False,
                    regex=True
                )

                ]

            print("AFTER WATCH MEN FILTER =", len(results))

        elif intent["gender"] == "women":

            results = results[

                results["product_name"]
                .fillna('')
                .str.contains(
                    r'for women|women|girls',
                    case=False,
                    na=False,
                    regex=True
                )

            ]

            print("AFTER WATCH WOMEN FILTER =", len(results))

    # SPECIAL BAG TYPES

    if intent["type"] == "sling":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                "sling",
                case=False,
                na=False
            )

        ]

        print("AFTER SLING FILTER =", len(results))

    elif intent["type"] == "backpack":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                "backpack",
                case=False,
                na=False
            )

        ]

        print("AFTER BACKPACK FILTER =", len(results))

    elif intent["type"] == "laptop":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'laptop',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER LAPTOP FILTER =", len(results))

    elif intent["type"] == "top":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'top|tops',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER TOP FILTER =", len(results))

    elif intent["type"] in ["pants", "trouser", "trousers"]:

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'pant|pants|trouser|trousers',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER PANTS FILTER =", len(results))

    elif intent["type"] == "shampoo":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'shampoo',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER SHAMPOO FILTER =", len(results))

    elif intent["type"] == "top":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'top',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER TOP FILTER =", len(results))

    elif intent["type"] == "wallet":

        results = results[
            results["product_name"]
            .fillna("")
            .str.contains(
                r"\bwallet\b|\bwallets\b",
                case=False,
                na=False,
                regex=True
            )
        ]

        print("AFTER WALLET FILTER =", len(results))

    elif intent["type"] in ["handbag", "handbags"]:

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'handbag|hand bag|shoulder bag|tote',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER HANDBAG FILTER =", len(results))

    elif intent["type"] == "belt":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'belt',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER BELT FILTER =", len(results))

    elif intent["type"] == "perfume":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'perfume|fragrance|deodorant|body spray',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER PERFUME FILTER =", len(results))

    elif intent["type"] == "lipstick":

        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'lipstick|lip color|lip colour',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER LIPSTICK FILTER =", len(results))
    # Office queries should not be restricted to shirts only
    if (
            intent.get("occasion") == "office"
            and intent.get("type") == "shirt"
    ):
        intent["type"] = None

    # TYPE

    if (
            intent["type"]
            and
            intent["type"] != intent["category"]
            and
            intent["category"] != "watches"
            and
            intent["type"] not in [

                "sling",
                "backpack",
                "laptop",
                "shoulder",
                "shampoo",
                "top",
                "pants",
                "trouser",
                "trousers",
                "wallet",
                "belt",
                "handbag",
                "handbags",
                "perfume",
                "lipstick"

            ]
        ):

        results = results[

            results["type_feature"]
            .fillna('')
            .str.contains(
                intent["type"],
                case=False,
                na=False
            )

        ]

        print("AFTER TYPE =", len(results))

        print("\nJEANS SAMPLE:")
        print(
            results[
                ["product_name", "gender_feature"]
            ]
            .head(20)
            .to_string()
        )

    # OCCASION

    if intent["occasion"]:

        if intent["occasion"] == "gift":
            results = results[

                results["product_name"]
                .fillna("")
                .str.contains(
                    r'watch|bag|wallet|belt|perfume|jewellery|necklace|earring|bracelet',
                    case=False,
                    na=False,
                    regex=True
                )

            ]

            print("AFTER GIFT FILTER =", len(results))


        # Skip occasion filtering for bags
        if intent["category"] == "bags":

            if intent["occasion"] == "office":

                results["office_score"] = (
                    results["product_name"]
                    .fillna("")
                    .str.contains(
                        r'laptop|shoulder|tote|handbag',
                        case=False,
                        regex=True
                    )
                    .astype(int)
                )

                # Remove party-style bags
                results = results[

                    ~

                    results["product_name"]
                    .fillna('')
                    .str.contains(
                        r'clutch|potli|party|suspenders|card holder',
                        case=False,
                        na=False,
                        regex=True
                    )

                ]
                results = results[

                    ~

                    results["product_name"]
                    .fillna("")
                    .str.contains(
                        r'bra|lingerie|kids|boy''s|girl''s|t-shirt',
                        case=False,
                        na=False,
                        regex=True
                    )

                ]

                print("AFTER OFFICE BAG FILTER =", len(results))


            elif intent["occasion"] == "college":

                results = results[

                    results["product_name"]
                    .fillna('')
                    .str.contains(
                        r'backpack|canvas|casual|sling|shoulder',
                        case=False,
                        na=False,
                        regex=True
                    )

                ]

                print("AFTER COLLEGE BAG FILTER =", len(results))

        else:

            keywords = occasion_map.get(
                intent["occasion"],
                []
            )

            if keywords:

                # Skip office filtering for clothing
                if (
                        intent["occasion"] == "office"
                        and
                        intent["category"] == "clothing"
                ):

                    results["office_score"] = (

                        results["product_name"]
                        .fillna("")
                        .str.contains(
                            r'formal|waistcoat|blazer|trouser',
                            case=False,
                            regex=True
                        )

                    ).astype(int)

                    results = results.sort_values(
                        by=["office_score", "rating"],
                        ascending=False
                    )

                    print("OFFICE CLOTHING BOOST APPLIED")
                    results = results[
                        ~results['gender_feature']
                        .fillna('')
                        .str.contains('boys|girls|kids', case=False, na=False)
                    ]

                else:

                    if (
                            intent["occasion"] == "interview"
                            and
                            intent["category"] == "clothing"
                    ):

                        results = results[

                            results["product_name"]
                            .fillna("")
                            .str.contains(
                                r'formal|waistcoat',
                                case=False,
                                na=False,
                                regex=True
                            )

                        ]

                        results = results[

                            ~results["product_name"]
                            .fillna("")
                            .str.contains(
                                r'tshirt|t-shirt|sweatshirt|hoodie|boys|girls|kids',
                                case=False,
                                na=False,
                                regex=True
                            )

                        ]

                        print("AFTER INTERVIEW FILTER =", len(results))

                    else:

                        pattern = "|".join(keywords)

                        filtered = results[
                            results["type_feature"]
                            .fillna("")
                            .str.contains(
                                pattern,
                                case=False,
                                na=False,
                                regex=True
                            )
                            |
                            results["product_name"]
                            .fillna("")
                            .str.contains(
                                pattern,
                                case=False,
                                na=False,
                                regex=True
                            )
                            ]

                        print("AFTER OCCASION =", len(filtered))

                        # Only apply the occasion filter if it finds products.
                        # Otherwise, keep the previous results.
                        if not filtered.empty:
                            results = filtered

                    if (
                            intent["occasion"] == "travel"
                            and
                            intent["category"] == "clothing"
                    ):
                        results = results[

                            ~

                            results["product_name"]
                            .fillna("")
                            .str.contains(
                                r'bra|lingerie|innerwear',
                                case=False,
                                na=False,
                                regex=True
                            )

                        ]

                        print("AFTER TRAVEL CLEANUP =", len(results))


    # COLLEGE FOOTWEAR CLEANUP

    if (

            intent["occasion"] == "college"

            and

            intent["category"] == "footwear"

    ):
        results = results[

            ~

            results["product_name"]
            .fillna('')
            .str.contains(
                "football|cricket|training|gym",
                case=False,
                na=False,
                regex=True
            )

        ]

    # DAILY WALKING FOOTWEAR

    if (
            intent["occasion"] == "daily"
            and
            intent["category"] == "footwear"
    ):
        results = results[

            results["product_name"]
            .fillna("")
            .str.contains(
                r'walking|running|sports',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER DAILY FOOTWEAR =", len(results))

    # GENERAL CLOTHING CLEANUP

    if intent["category"] == "clothing":
        results = results[

            ~

            results["product_name"]
            .fillna("")
            .str.contains(
                r'bra|lingerie|innerwear',
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER CLOTHING CLEANUP =", len(results))

    # OFFICE FOOTWEAR CLEANUP

    if (
            intent.get("occasion") == "office"
            and
            intent.get("category") == "footwear"
    ):
        results = results[

            ~

            results["product_name"]
            .fillna("")
            .str.contains(
                r"slipper|flip flop|flip-flop|Flip Flops|Running Shoes",
                case=False,
                na=False,
                regex=True
            )

        ]

        print("AFTER OFFICE FOOTWEAR CLEANUP =", len(results))

    # BUDGET

    print("BUDGET =", intent["budget"])

    budget = intent.get("budget")

    if budget:
        budget = int(budget)

        results = results[
            results["price"] <= budget
            ]
        print(results[["product_name", "type_feature"]].head(20))



    if intent["type"] == "kurta":
        print(
            results[
                ["product_name", "category", "type_feature"]
            ].head(20)
        )

    sort_columns = ["rating"]

    if "office_score" in results.columns:
        sort_columns = ["office_score", "rating"]

    print("FINAL RESULT COUNT =", len(results))

    return (

        results

        .sort_values(
            by=sort_columns,
            ascending=False
        )

        .drop_duplicates(
            subset="product_name"
        )

        .head(5)

    )