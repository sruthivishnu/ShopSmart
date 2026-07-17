from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from recommendation.search import (
    search_products
)

from recommendation.hybrid import (
    hybrid_recommendation
)

from recommendation.model import (
    products_df
)

from recommendation.user_recommendation import (
    get_user_recommendations
)
from recommendation.recently_viewed import (
    get_recently_viewed
)

from recommendation.purchase_history import (
    get_purchase_history
)

from recommendation.apriori import (
    get_apriori_recommendations
)

from recommendation.chatbot_intent import (
    extract_chatbot_intent
)

from recommendation.chatbot_ai import (
    extract_ai_intent
)

from recommendation.chatbot_search import (
    chatbot_search
)

from recommendation.chatbot_router import (
    route_query
)

from recommendation.chatbot_faq import (
    get_faq_response
)

from recommendation.chatbot_greetings import (
    get_greeting
)

from recommendation.chatbot_help import (
    get_help
)

from recommendation.chatbot_gemini import (
    get_gemini_response
)

from recommendation.chatbot_handlers import (
    handle_personalized,
    handle_orders,
    handle_deals,
    handle_greeting,
    handle_help
)

from recommendation.chatbot_combo import (
    handle_combo
)

from recommendation.chatbot_shopping import (
    handle_shopping
)

import recommendation.chatbot_search

from recommendation.homepage import (
    get_top_deals,
    get_hot_picks,
    get_fashion_deals,
    get_footwear_products,
    get_bags_products,
    get_furniture_products,
    get_watch_products,
    get_beauty_products
)

from recommendation.category_helper import (
    build_subcategory_page
)

from recommendation.category_subtypes import CATEGORY_SUBTYPES

from flask import redirect


import os

import google.generativeai as genai

from dotenv import load_dotenv

from flask_mysqldb import MySQL

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "shopsmart_secret_key"
)

app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")

app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")

app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")

app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

app.config["MYSQL_PORT"] = int(
    os.getenv("MYSQL_PORT", 3306)
)

mysql = MySQL(app)

print("MYSQL_HOST =", app.config["MYSQL_HOST"])
print("MYSQL_PORT =", app.config["MYSQL_PORT"])

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


@app.context_processor
def cart_count():

    count = 0

    if 'user_id' in session:

        cursor = mysql.connection.cursor()

        cursor.execute(
            '''
            SELECT SUM(quantity)
            FROM cart
            WHERE user_id=%s
            ''',
            (session['user_id'],)
        )

        result = cursor.fetchone()

        cursor.close()

        if result and result[0]:

            count = result[0]

    return dict(cart_count=count)
# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route('/', methods=['GET', 'POST'])
def home():

    search_results = None



    personal_recommendations = []

    recently_viewed_products = []
    purchase_history = []

    premium_categories = [
        'watches',
        'footwear',
        'jewellery',
        'bags',
        'clothing'
    ]

    import time

    used_ids = set()

    t = time.time()
    top_deals, used_ids = get_top_deals(used_ids)
    print("Top Deals:", round(time.time() - t, 2))

    t = time.time()
    trending_products, used_ids = get_hot_picks(used_ids)
    print("Hot Picks:", round(time.time() - t, 2))

    t = time.time()
    footwear_products, used_ids = get_footwear_products(used_ids)
    print("Footwear:", round(time.time() - t, 2))

    t = time.time()
    bags_products, used_ids = get_bags_products(used_ids)
    print("Bags:", round(time.time() - t, 2))

    t = time.time()
    furniture_products, used_ids = get_furniture_products(used_ids)
    print("Furniture:", round(time.time() - t, 2))

    t = time.time()
    watch_products, used_ids = get_watch_products(used_ids)
    print("Watches:", round(time.time() - t, 2))

    t = time.time()
    beauty_products, used_ids = get_beauty_products(used_ids)
    print("Beauty:", round(time.time() - t, 2))

    t = time.time()
    fashion_deals, used_ids = get_fashion_deals(used_ids)
    print("Fashion:", round(time.time() - t, 2))

    if request.method == 'POST':

        keyword = request.form.get(
            'keyword'
        )

        if keyword:

            search_results = (
                search_products(keyword)
            )

    if 'user_id' in session:
        personal_recommendations = (
            get_user_recommendations(
                session['user_id'],
                mysql
            )
        )

        recently_viewed_products = (
            get_recently_viewed(
                session['user_id'],
                mysql
            )
        )

        purchase_history = (
            get_purchase_history(
                session['user_id'],
                mysql
            )
        )

    return render_template(
        'index.html',
        search_results=search_results,
        personal_recommendations=personal_recommendations,
        recently_viewed_products=recently_viewed_products,
        trending_products=trending_products,
        purchase_history=purchase_history,
        top_deals=top_deals,
        footwear_products=footwear_products,
        bags_products=bags_products,
        furniture_products=furniture_products,
        watch_products=watch_products,
        beauty_products=beauty_products,
        fashion_deals = fashion_deals
    )


@app.route('/category/<category_name>')
def category_page(category_name):
    if category_name == "all":
        categories = [

            'Men Fashion',

            'Women Fashion',

            'Kids Fashion',

            'Footwear',

            'Bags & Wallets',

            'Furniture',

            'Pet Supplies',

            'Sports',

            'Jewellery',

            'Watches',

            'Beauty & Personal Care',

            'Pens & Stationery',

            'Home Furnishing',

            'Home Decor',

            'Automotive',

            'Tools & Hardware'

        ]

        return render_template(
            'all_categories.html',
            categories=categories
        )
    # -----------------------------------
    # MEN / WOMEN / KIDS
    # -----------------------------------

    if category_name in ["men", "women", "kids"]:

        products = products_df.copy()

        if category_name == "men":

            products = products[
                products["gender_feature"]
                .str.contains(
                    r"\bmen\b|\bman's\b",
                    case=False,
                    regex=True,
                    na=False
                )
            ]

        elif category_name == "women":

            products = products[
                products["gender_feature"]
                .str.contains("women", case=False, na=False)
            ]

        else:

            products = products[
                products["gender_feature"]
                .str.contains(
                    r"kids|boy|girl",
                    case=False,
                    na=False,
                    regex=True
                )
            ]

        # Clothing only
        products = products[
            products["category"]
            .str.contains(
                "clothing",
                case=False,
                na=False
            )
        ]

        # -----------------------------------
        # REMOVE UNWANTED SUBCATEGORIES
        # -----------------------------------

        if category_name == "men":

            IGNORE_TYPES = {

                # Generic
                "other",
                "combo",
                "kit",
                "accessory",

                # Irrelevant
                "cup",
                "pencil",
                "cream",

                # Accessories
                "glove",
                "tie",
                "scarf",
                "cap",

                # Women's Fashion
                "dress",
                "top",
                "leggings",
                "skirt",
                "dupatta",
                "nighty",
                "tunic",
                "shrug",
                "jumpsuit",
                "jeggings",
                "capri",
                "blouse",
                "kaftan",
                "bra",
                "lingerie",
                "dungaree"

            }

        elif category_name == "women":

            IGNORE_TYPES = {

                "other",
                "combo",
                "kit",
                "accessory",
                "kaftan",
                "dungaree",
                "glove",

                "cup",
                "pencil"

            }

            # Remove innerwear products that may have
            # incorrect type_feature values

            products = products[

                ~

                products["product_name"]

                .str.contains(

                    r"bra|lingerie|sports bra|t-shirt bra|camisole|innerwear|underwear|panty|brief",

                    case=False,

                    na=False,

                    regex=True

                )

            ]

        else:

            IGNORE_TYPES = {

                "other",
                "combo",
                "kit",
                "accessory"

            }

        products = products[
            ~products["type_feature"].isin(IGNORE_TYPES)
        ]

        # -----------------------------------
        # REMOVE PRODUCTS WITHOUT REAL IMAGES
        # -----------------------------------

        products = products[
            products["image"].notna()
        ]

        products = products[
            ~products["image"].str.contains(
                r"default|no_image",
                case=False,
                na=False,
                regex=True
            )
        ]

        # Build subcategories
        subcategories = (
            products["type_feature"]
            .value_counts()
            .reset_index()
        )

        subcategories.columns = [
            "type",
            "count"
        ]

        subcategories = subcategories.to_dict("records")

        from recommendation.subcategory_images import (
            SUBCATEGORY_IMAGES,
            IMAGE_MAP
        )

        for item in subcategories:

            product_type = item["type"]

            # Default image
            image = SUBCATEGORY_IMAGES.get(
                product_type,
                "default.jpg"
            )

            # Gender specific image
            if category_name in IMAGE_MAP:
                image = IMAGE_MAP[category_name].get(
                    product_type,
                    image
                )

            item["image"] = image

            # -------------------------
            # Gender-specific images
            # -------------------------

            if category_name == "men":

                if item["type"] == "shirt":
                    image = "shirt_men.jpg"

                elif item["type"] == "kurta":
                    image = "kurta_men.jpg"

                elif item["type"] == "shoe":
                    image = "shoe_men.jpg"

                elif item["type"] == "watch":
                    image = "watch_men.jpg"

                elif item["type"] == "wallet":
                    image = "wallet_men.jpg"

            elif category_name == "women":

                if item["type"] == "shirt":
                    image = "shirt_women.jpg"

                elif item["type"] == "kurta":
                    image = "kurta_women.jpg"

                elif item["type"] == "shoe":
                    image = "shoe_women.jpg"

                elif item["type"] == "watch":
                    image = "watch_women.jpg"

                elif item["type"] == "wallet":
                    image = "wallet_women.jpg"

            item["image"] = image

        hero_images = {

            "men": "images/categories/men.jpg",

            "women": "images/categories/women.jpg",

            "kids": "images/categories/kids.jpg"

        }

        return build_subcategory_page(

            category_name=category_name,

            display_name=category_name.title() + " Fashion",

            products=products,

            hero_image=hero_images[category_name]

        )

    elif category_name == "footwear":

        products = products_df[
            products_df["category"]
            .str.contains(
                "footwear",
                case=False,
                na=False
            )
        ]

        products = products[
            products["image"].notna()
        ]

        products = products[
            ~products["image"]
            .str.contains(
                r"default|no_image",
                case=False,
                na=False,
                regex=True
            )
        ]

        return build_subcategory_page(

            category_name="footwear",

            display_name="Footwear",

            products=products,

            hero_image="images/categories/footwear.jpg"

        )


    # -----------------------------------
    # BAGS
    # -----------------------------------

    elif category_name == "bags":

        products = products_df[
            products_df["category"]
            .str.contains(
                "bags",
                case=False,
                na=False
            )
        ]

        products = products[
            products["image"].notna()
        ]

        products = products[
            ~products["image"]
            .str.contains(
                r"default|no_image",
                case=False,
                na=False,
                regex=True
            )
        ]

        return build_subcategory_page(

            category_name="bags",

            display_name="Bags & Wallets",

            products=products,

            hero_image="images/categories/bags.jpg"

        )


    # -----------------------------------
    # FURNITURE
    # -----------------------------------

    elif category_name == "furniture":

        products = products_df[
            products_df["category"]
            .str.contains(
                "furniture",
                case=False,
                na=False
            )
        ]

        products = products[
            products["image"].notna()
        ]

        products = products[
            ~products["image"]
            .str.contains(
                r"default|no_image",
                case=False,
                na=False,
                regex=True
            )
        ]

        return build_subcategory_page(

            category_name="furniture",

            display_name="Furniture",

            products=products,

            hero_image="images/categories/furniture.jpg"

        )

    elif category_name in ["home-furnishing"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                "Home Furnishing",

                case=False,

                na=False

            )

        ]

    elif category_name in ["home-decor"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                "Home Decor",

                case=False,

                na=False

            )

        ]

    elif category_name == "jewellery":

        products = products_df[

            products_df["category"]

            .str.contains(

                "jewellery",

                case=False,

                na=False

            )

        ]

    elif category_name in ["pens", "pens-stationery"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                r"Pens & Stationery",

                case=False,

                na=False,

                regex=True

            )

        ]

    elif category_name in ["tools", "tools-hardware"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                r"Tools|Hardware",

                case=False,

                na=False,

                regex=True

            )

        ]

    elif category_name == "sports":

        products = products_df[
            products_df['category']
            .str.contains(
                "Sports",
                case=False,
                na=False
            )
        ]

    elif category_name == "automotive":

        products = products_df[

            products_df["category"]

            .str.contains(

                "Automotive",

                case=False,

                na=False

            )

        ]



    elif category_name == "watches":

        products = products_df[
            products_df["category"]
            .str.contains(
                "watch",
                case=False,
                na=False
            )
        ]

    elif category_name in ["pets", "pet-supplies"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                "Pet Supplies",

                case=False,

                na=False

            )

        ]

    elif category_name in ["beauty", "beauty-personal-care"]:

        products = products_df[

            products_df["category"]

            .str.contains(

                r"beauty|personal care",

                case=False,

                na=False,

                regex=True

            )

        ]


        return build_subcategory_page(

            category_name="beauty",

            display_name="Beauty & Personal Care",

            products=products,

            hero_image="images/categories/beauty.jpg"

        )



    elif category_name == "fashion":

        products = products_df[

            products_df['product_name']
            .str.contains(
                r'shirt|dress|top|kurta|jeans|tshirt|shoe|shoes|boot|boots|heel|sandal|bag|clutch|jacket',
                case=False,
                na=False,
                regex=True
            )

            &

            ~

            products_df['product_name']
            .str.contains(
                r'bra|lingerie|sports bra|bellies|ballerina|T-shirt bra|t-shirt bra|innerwear|underwear|panty|brief|camisole|T-Shirt',
                case=False,
                na=False,
                regex=True
            )

        ]

    else:

        products = products_df.head(20)

    products = products.head(100)

    hero_images = {

        "sports": "images/categories/sports.jpg",

        "pets": "images/categories/pets.jpg",

        "pet-supplies": "images/categories/pets.jpg",

        "jewellery": "images/categories/jewellery.jpg",

        "watches": "images/categories/watches.jpg",

        "beauty": "images/categories/beauty.jpg",

        "beauty-personal-care": "images/categories/beauty.jpg",

        "pens": "images/categories/pens.jpg",

        "pens-stationery": "images/categories/pens.jpg",

        "home-furnishing": "images/categories/home.jpg",

        "home-decor": "images/categories/decor.jpg",

        "automotive": "images/categories/automotive.jpg",

        "tools": "images/categories/tools.jpg",

        "tools-hardware": "images/categories/tools.jpg"

    }

    products = products[

        products["image"]

        .notna()

    ]

    products = products[

        ~products["image"]

        .str.contains(

            "default",

            case=False,

            na=False

        )

    ]

    products = products.head(100)

    return render_template(

        "category_premium.html",

        category_name=category_name.title(),

        products=products.to_dict("records"),

        hero_image=url_for(

            "static",

            filename=hero_images.get(

                category_name,

                "images/categories/banner.jpg"

            )

        )

    )

@app.route('/category/general/<path:category>')
def general_category(category):

    redirect_map = {

        "Men Fashion": "men",
        "Women Fashion": "women",
        "Kids Fashion": "kids",

        "Footwear": "footwear",
        "Bags & Wallets": "bags",
        "Furniture": "furniture",

        "Sports": "sports",
        "Pet Supplies": "pets",

        "Jewellery": "jewellery",
        "Beauty & Personal Care": "beauty",

        "Watches": "watches",

        "Pens & Stationery": "pens",
        "Home Furnishing": "home-furnishing",
        "Home Decor": "home-decor",
        "Automotive": "automotive",
        "Tools & Hardware": "tools-hardware"

    }

    if category in redirect_map:
        return redirect(

            url_for(

                "category_page",

                category_name=redirect_map[category]

            )

        )

    products = products_df.copy()

    # ----------------------------
    # CATEGORY FILTER
    # ----------------------------

    if category == "Jewellery":

        products = products[
            products["category"]
            .str.contains(
                "jewellery",
                case=False,
                na=False
            )
        ]

    elif category == "Beauty & Personal Care":

        products = products[
            products["category"]
            .str.contains(
                r"beauty|personal care",
                case=False,
                na=False,
                regex=True
            )
        ]

    elif category == "Pens & Stationery":

        products = products[
            products["category"]
            .str.contains(
                r"pen|stationery",
                case=False,
                na=False,
                regex=True
            )
        ]

    elif category == "Home Furnishing":

        products = products[
            products["category"]
            .str.contains(
                "home furnishing",
                case=False,
                na=False
            )
        ]

    elif category == "Home Decor":

        products = products[
            products["category"]
            .str.contains(
                "home decor",
                case=False,
                na=False
            )
        ]

    elif category == "Automotive":

        products = products[
            products["category"]
            .str.contains(
                "automotive",
                case=False,
                na=False
            )
        ]

    elif category == "Tools & Hardware":

        products = products[
            products["category"]
            .str.contains(
                r"tools|hardware",
                case=False,
                na=False,
                regex=True
            )
        ]

    else:

        products = products[
            products["category"]
            .str.contains(
                category,
                case=False,
                na=False
            )
        ]

    # ----------------------------
    # Remove products without images
    # ----------------------------

    products = products[
        products["image"].notna()
    ]

    products = products[
        ~products["image"]
        .str.contains(
            "default",
            case=False,
            na=False
        )
    ]

    products = products.drop_duplicates(
        subset="product_name"
    )

    products = products.head(100)

    # ----------------------------
    # Hero Images
    # ----------------------------

    hero_images = {

        "Jewellery":"images/categories/jewellery.jpg",

        "Beauty & Personal Care":"images/categories/beauty.jpg",

        "Pens & Stationery":"images/categories/pens.jpg",

        "Home Furnishing":"images/categories/home.jpg",

        "Home Decor":"images/categories/decor.jpg",

        "Automotive":"images/categories/automotive.jpg",

        "Tools & Hardware":"images/categories/tools.jpg"

    }

    return render_template(

        "category_premium.html",

        category_name=category,

        products=products.to_dict("records"),

        hero_image=url_for(

            "static",

            filename=hero_images.get(

                category,

                "images/categories/banner.jpg"

            )

        )

    )

# -----------------------------------
# CATEGORY SUBTYPES
# -----------------------------------

@app.route('/category/<gender>/<product_type>')
def category_subtype(gender, product_type):
    product_type = product_type.replace("_", " ")

    print("URL TYPE =", product_type)
    products = products_df.copy()

    # -------------------------
    # GENDER FILTER
    # -------------------------

    if gender == "men":

        products = products[
            products["gender_feature"] == "men"
        ]

        products = products[
            ~products["product_name"].str.contains(
                r"\bwomen\b|\bwomen's\b|\bladies\b",
                case=False,
                regex=True,
                na=False
            )
        ]


    elif gender == "women":

        products = products[
            products["gender_feature"] == "women"
            ]

        products = products[
            ~products["product_name"].str.contains(
                r"\bmen\b|\bman's\b",
                case=False,
                regex=True,
                na=False
            )
        ]



    elif gender == "kids":

        products = products[

            products["gender_feature"].isin(
                ["kids", "boys", "girls"]
            )

        ]


    # -------------------------
    # CATEGORY FILTER
    # -------------------------

    if gender == "bags":

        products = products[
            products["category"]
            .str.contains(
                "bags",
                case=False,
                na=False
            )
        ]

    elif gender == "footwear":

        products = products[
            products["category"]
            .str.contains(
                "footwear",
                case=False,
                na=False
            )
        ]

    elif gender == "furniture":

        products = products[
            products["category"]
            .str.contains(
                "furniture",
                case=False,
                na=False
            )
        ]

    # -------------------------
    # PRODUCT TYPE FILTER
    # -------------------------

    # Fashion pages still use type_feature
    if gender in ["men", "women", "kids"]:

        normalized_type = (
            product_type
            .lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

        products = products[
            products["type_feature"]
            .fillna("")
            .str.lower()
            .str.replace("_", "", regex=False)
            .str.replace("-", "", regex=False)
            .str.replace(" ", "", regex=False)
            ==
            normalized_type
            ]

        # -----------------------------------
        # PRODUCT TYPE CLEANUP
        # -----------------------------------

        if normalized_type == "shirt":

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

        elif normalized_type == "tshirt":

            products = products[
                ~products["product_name"]
                .fillna("")
                .str.lower()
                .str.contains(
                    r"sweatshirt|hoodie|blouse|kurti|top|tunic|sweater",
                    regex=True,
                    na=False
                )
            ]

    # Other categories use product_name keywords
    else:

        keywords = CATEGORY_SUBTYPES.get(gender, {}).get(product_type, [])

        if keywords:

            mask = False

            for word in keywords:
                mask = (
                        mask
                        |
                        products["product_name"]
                        .str.contains(
                            word,
                            case=False,
                            na=False,
                            regex=False
                        )
                )

            products = products[mask]

            # -----------------------------------
            # CLEAN CATEGORY RESULTS
            # -----------------------------------

            if gender == "bags":

                if product_type == "wallet":

                    products = products[
                        ~products["product_name"]
                        .str.contains(
                            r"belt|suspender",
                            case=False,
                            regex=True,
                            na=False
                        )
                    ]

                elif product_type == "bags":

                    products = products[
                        ~products["product_name"]
                        .str.contains(
                            r"belt|suspender|potli|organizer|keeper",
                            case=False,
                            regex=True,
                            na=False
                        )
                    ]


            elif gender == "furniture" and product_type == "bed":

                products = products[
                    ~products["product_name"]
                    .str.contains(
                        r"pet|dog|cat|puppy|kitten",
                        case=False,
                        regex=True,
                        na=False
                    )
                ]


            elif gender == "beauty":

                if product_type == "shampoo":

                    products = products[
                        ~products["product_name"]
                        .str.contains(
                            r"dog|pet|puppy|cat|animal",
                            case=False,
                            regex=True,
                            na=False
                        )
                    ]

                elif product_type == "cream":

                    products = products[
                        ~products["product_name"]
                        .str.contains(
                            r"shoe cream|cream color|cream coloured|bra|loafer|blanket",
                            case=False,
                            regex=True,
                            na=False
                        )
                    ]

    print("URL TYPE =", product_type)

    # -----------------------------------
    # REMOVE WRONG PRODUCTS
    # -----------------------------------

    EXCLUDE_KEYWORDS = {

        "shirt": [
            "bra",
            "lingerie",
            "camisole",
            "innerwear",
            "underwear",
            "sports bra",
            "t-shirt bra"
        ],

        "tshirt": [
            "bra",
            "lingerie",
            "camisole",
            "innerwear",
            "underwear",
            "sports bra",
            "t-shirt bra"
        ],

        "shorts": [
            "top",
            "tunic",
            "blouse"
        ],

        "trackpant": [
            "top",
            "tunic",
            "blouse"
        ],

        "leggings": [
            "top",
            "tunic",
            "blouse"
        ]

    }

    if product_type.lower() in EXCLUDE_KEYWORDS:
        pattern = "|".join(
            EXCLUDE_KEYWORDS[
                product_type.lower()
            ]
        )

        products = products[
            ~products["product_name"]
            .str.contains(
                pattern,
                case=False,
                regex=True,
                na=False
            )
        ]

    # -----------------------------------
    # REMOVE PRODUCTS WITHOUT REAL IMAGES
    # -----------------------------------

    products = products[
        products["image"].notna()
    ]

    products = products[
        ~products["image"]
        .str.contains(
            r"default|no_image",
            case=False,
            na=False,
            regex=True
        )
    ]

    products = (

        products

        .drop_duplicates(
            subset="product_name"
        )

        .head(100)

    )

    return render_template(

        "category.html",

        category_name=f"{gender.title()} {product_type.title()}",

        products=products.to_dict("records")

    )


# -----------------------------------
# AUTOCOMPLETE API
# -----------------------------------
@app.route('/autocomplete')
def autocomplete():

    query = request.args.get(
        'q',
        ''
    ).lower().strip()

    if not query:

        return jsonify([])

    suggestions = set()

    # product names

    product_matches = products_df[

        products_df['product_name']
        .str.lower()
        .str.contains(
            query,
            na=False
        )

    ]['product_name'].head(5)

    # subcategories

    sub_matches = products_df[

        products_df['subcategory']
        .str.lower()
        .str.contains(
            query,
            na=False
        )

    ]['subcategory'].head(5)

    for item in product_matches:

        suggestions.add(item)

    for item in sub_matches:
        item = str(item)

        item = item.replace('["', '')

        item = item.replace('"]', '')

        parts = item.split(">>")

        suggestions.add(
            parts[-1].strip()
        )

    return jsonify(
        list(suggestions)[:8]
    )


# -----------------------------------
# EXTRACT CORE SEARCH KEYWORDS
# -----------------------------------

# -----------------------------------
# EXTRACT CORE SEARCH KEYWORDS
# -----------------------------------

import re

def extract_core_keyword(query):

    query = query.lower()

    # Remove possessive forms
    query = re.sub(r"\b(men|women|man|woman|boy|boys|girl|girls|kid|kids)'s\b", "", query)

    # Remove gender words
    query = re.sub(
        r"\b(for|men|man|women|woman|boys|boy|girls|girl|kids|kid)\b",
        " ",
        query
    )

    # Remove extra spaces
    query = re.sub(r"\s+", " ", query)

    return query.strip()

@app.route('/search')
def search_page():

    query = request.args.get(
        'q',
        ''
    ).lower().strip()

    if query == "trending":
        products = products_df.copy()

        products = products[
            products["image"] != "images/default.jpg"
            ]

        products = (
            products
            .drop_duplicates(subset="product_name")
            .sort_values(
                by=["rating", "reviews"],
                ascending=False
            )
            .head(100)
        )

        return render_template(

            'search_results.html',

            query="Trending Products",

            products=products.to_dict('records')

        )

    if query == "under 2000":
        products = products_df[
            products_df["price"] < 2000
            ]

        products = products[
            products["image"] != "images/default.jpg"
            ]

        products = (
            products
            .drop_duplicates(subset="product_name")
            .sort_values(
                by=["rating", "reviews"],
                ascending=False
            )
            .head(100)
        )

        return render_template(

            'search_results.html',

            query="Products Under ₹2000",

            products=products.to_dict('records')

        )

    products = products_df.copy()


    # -------------------------
    # GENDER FILTER
    # -------------------------

    if 'women' in query:

        products = products[
            products['gender_feature']
            .str.contains(
                r'\bwomen\b|\bwoman\b|\bladies\b',
                case=False,
                na=False,
                regex=True
            )
        ]

    elif 'men' in query:

        products = products[
            products['gender_feature']
            .str.contains(
                r'\bmen\b|\bman\b',
                case=False,
                na=False,
                regex=True
            )
        ]

    elif any(word in query for word in ['boys', 'boy']):

        products = products[
            products['gender_feature']
            .str.contains(
                r'\bboys\b|\bboy\b',
                case=False,
                na=False,
                regex=True
            )
        ]

    elif any(word in query for word in ['girls', 'girl']):

        products = products[
            products['gender_feature']
            .str.contains(
                r'\bgirls\b|\bgirl\b',
                case=False,
                na=False,
                regex=True
            )
        ]

    elif any(word in query for word in ['kids', 'kid']):

        products = products[
            products['gender_feature']
            .str.contains(
                r'\bkids\b|\bkid\b|\bboys\b|\bboy\b|\bgirls\b|\bgirl\b',
                case=False,
                na=False,
                regex=True
            )
        ]

    # -------------------------
    # REMOVE COMMON WORDS
    # -------------------------

    clean_query = extract_core_keyword(
        query
    )

    # -------------------------
    # SEARCH PRODUCTS
    # -------------------------

    if clean_query:

        words = clean_query.split()

        mask = True

        for word in words:
            mask = (

                    mask &

                    products['search_text'].str.contains(
                        word,
                        case=False,
                        na=False,
                        regex=False
                    )

            )

        products = products[mask]

    # -----------------------------------
    # KEEP ONLY PRODUCTS WITH REAL IMAGES
    # -----------------------------------

    products = products[
        products["image"].notna()
    ]

    products = products[
        products["image"] != "images/default.jpg"
        ]

    # -----------------------------------
    # REMOVE DUPLICATES
    # -----------------------------------

    products = (
        products
        .drop_duplicates(subset="product_name")
    )

    # -----------------------------------
    # SHOW BEST PRODUCTS FIRST
    # -----------------------------------

    products = (
        products
        .sort_values(
            by=["rating", "reviews"],
            ascending=False
        )
        .head(100)
    )

    return render_template(

        'search_results.html',

        query=query,

        products=
        products.to_dict('records')

    )

# -----------------------------------
# PRODUCT RECOMMENDATION PAGE
# -----------------------------------

@app.route('/recommend/<int:product_id>')
def recommend(product_id):

    # selected product
    selected_product = products_df[

        products_df['product_id']
        == product_id

    ]

    # product not found
    if selected_product.empty:

        return render_template(
            'recommend.html',
            selected_product=None,
            recommendation_sections={}
        )

    selected_product = (
        selected_product.iloc[0]
    )

    # SAVE RECENTLY VIEWED PRODUCT

    if 'user_id' in session:
        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            DELETE
            FROM recently_viewed
            WHERE user_id = %s
              AND product_id = %s
            """,
            (
                session['user_id'],
                product_id
            )
        )

        cursor.execute(
            """
            INSERT INTO recently_viewed(user_id,
                                        product_id)

            VALUES (%s, %s)
            """,
            (
                session['user_id'],
                product_id
            )
        )

        mysql.connection.commit()

        cursor.close()

    def get_fashion_categories():
        return [
            "clothing",
            "footwear",
            "watches",
            "bags, wallets & belts",
            "jewellery"
        ]

    # AMAZON STYLE RECOMMENDATIONS
    recommendation_sections = (
        hybrid_recommendation(
            user_id=1,
            product_id=product_id,
            top_n=8
        )
    )

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT
            AVG(rating),
            COUNT(*)
        FROM product_reviews
        WHERE product_id=%s
        ''',
        (product_id,)
    )

    rating_data = cursor.fetchone()

    dataset_rating = float(
        selected_product.get('rating', 0)
    )

    dataset_reviews = int(
        selected_product.get('reviews', 0)
    )

    average_rating = dataset_rating
    review_count = dataset_reviews

    if rating_data and rating_data[1] > 0:
        user_rating = float(rating_data[0])
        user_reviews = int(rating_data[1])

        average_rating = round(

            (
                    dataset_rating * dataset_reviews
                    +
                    user_rating * user_reviews
            )

            /

            (
                    dataset_reviews
                    +
                    user_reviews
            ),

            1
        )

        review_count = (
                dataset_reviews
                +
                user_reviews
        )

    cursor.execute(
        '''
        SELECT
            u.username,
            pr.rating,
            pr.review_text,
            pr.created_at

        FROM product_reviews pr

        JOIN users u
            ON pr.user_id = u.id

        WHERE pr.product_id=%s

        ORDER BY pr.created_at DESC LIMIT 3
        ''',
        (product_id,)
    )

    reviews = cursor.fetchall()

    cursor.close()

    return render_template(
        'recommend.html',
        selected_product=selected_product,
        recommendation_sections=recommendation_sections,
        average_rating=average_rating,
        review_count=review_count,
        reviews=reviews,
    )


# -----------------------------------
# SIGNUP
# -----------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']

        cursor = mysql.connection.cursor()

        # Check whether email already exists

        cursor.execute(
            '''
            SELECT id
            FROM users
            WHERE email=%s
            ''',
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:

            cursor.close()

            return render_template(
                'signup.html',
                error="Email already registered."
            )

        # Hash password

        hashed_password = generate_password_hash(password)

        # Insert new user

        cursor.execute(
            '''
            INSERT INTO users
            (
                username,
                email,
                password
            )

            VALUES (%s,%s,%s)
            ''',
            (
                username,
                email,
                hashed_password
            )
        )

        mysql.connection.commit()

        cursor.close()

        return redirect('/login')

    return render_template('signup.html')

# -----------------------------------
# LOGIN
# -----------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email'].strip().lower()
        password = request.form['password']

        print("Attempting MySQL connection...")

        cursor = mysql.connection.cursor()

        cursor.execute(
            '''
            SELECT id,
                   username,
                   email,
                   password
            FROM users
            WHERE email=%s
            ''',
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user[3], password):

            session['user_id'] = user[0]
            session['username'] = user[1]

            return redirect('/')

        return render_template(
            'login.html',
            error="Invalid Email or Password."
        )

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/')

# -----------------------------------
# ADD TO CART
# -----------------------------------

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT * FROM cart
        WHERE user_id=%s
        AND product_id=%s
        ''',
        (user_id, product_id)
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute(
            '''
            UPDATE cart
            SET quantity = quantity + 1
            WHERE user_id=%s
            AND product_id=%s
            ''',
            (user_id, product_id)
        )

    else:

        cursor.execute(
            '''
            INSERT INTO cart(
                user_id,
                product_id,
                quantity
            )

            VALUES(%s,%s,%s)
            ''',
            (user_id, product_id, 1)
        )

    mysql.connection.commit()

    cursor.close()

    return redirect(
        url_for(
            'recommend',
            product_id=product_id
        )
    )

# -----------------------------------
# CART PAGE
# -----------------------------------

@app.route('/cart')
def cart():

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT product_id,
               quantity
        FROM cart
        WHERE user_id=%s
        ''',
        (user_id,)
    )

    cart_items = cursor.fetchall()

    cursor.close()

    products = []

    total = 0

    for item in cart_items:

        product_id = item[0]
        quantity = item[1]

        product = products_df[
            products_df['product_id']
            == product_id
        ]

        if not product.empty:

            product = product.iloc[0]

            subtotal = (
                product.price * quantity
            )

            total += subtotal

            products.append({

                'product_id':
                    product.product_id,

                'product_name':
                    product.product_name,

                'price':
                    product.price,

                'quantity':
                    quantity,

                'subtotal':
                    subtotal,

                'image':
                    product.image

            })

    return render_template(
        'cart.html',
        products=products,
        total=total
    )
# -----------------------------------
# REMOVE FROM CART
# -----------------------------------

@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        DELETE FROM cart
        WHERE user_id=%s
        AND product_id=%s
        ''',
        (user_id, product_id)
    )

    mysql.connection.commit()

    cursor.close()

    return redirect('/cart')

# -----------------------------------
# INCREASE QUANTITY
# -----------------------------------

@app.route('/increase_quantity/<int:product_id>')
def increase_quantity(product_id):

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        UPDATE cart
        SET quantity = quantity + 1
        WHERE user_id=%s
        AND product_id=%s
        ''',
        (user_id, product_id)
    )

    mysql.connection.commit()

    cursor.close()

    return redirect('/cart')


# -----------------------------------
# DECREASE QUANTITY
# -----------------------------------

@app.route('/decrease_quantity/<int:product_id>')
def decrease_quantity(product_id):

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT quantity
        FROM cart
        WHERE user_id=%s
        AND product_id=%s
        ''',
        (user_id, product_id)
    )

    item = cursor.fetchone()

    if item:

        quantity = item[0]

        if quantity > 1:

            cursor.execute(
                '''
                UPDATE cart
                SET quantity = quantity - 1
                WHERE user_id=%s
                AND product_id=%s
                ''',
                (user_id, product_id)
            )

        else:

            cursor.execute(
                '''
                DELETE FROM cart
                WHERE user_id=%s
                AND product_id=%s
                ''',
                (user_id, product_id)
            )

    mysql.connection.commit()

    cursor.close()

    return redirect('/cart')

@app.route('/checkout')
def checkout():

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT product_id,
               quantity
        FROM cart
        WHERE user_id=%s
        ''',
        (user_id,)
    )

    cart_items = cursor.fetchall()

    for item in cart_items:

        product_id = item[0]
        quantity = item[1]

        cursor.execute(
            '''
            INSERT INTO orders(
                user_id,
                product_id,
                quantity
            )

            VALUES(%s,%s,%s)
            ''',
            (
                user_id,
                product_id,
                quantity
            )
        )

    cursor.execute(
        '''
        DELETE FROM cart
        WHERE user_id=%s
        ''',
        (user_id,)
    )

    mysql.connection.commit()

    cursor.close()

    return render_template(
        'order_success.html'
    )


@app.route('/orders')
def orders():

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT product_id,
               quantity,
               order_date
        FROM orders
        WHERE user_id=%s
        ORDER BY order_date DESC
        ''',
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()

    orders_data = []

    for row in rows:

        product_id = row[0]

        product = products_df[
            products_df['product_id'].astype(int)
            == int(product_id)
        ]


        if not product.empty:

            product = product.iloc[0]

            orders_data.append({

                'product_id':
                    product.product_id,

                'product_name':
                    product.product_name,

                'price':
                    product.price,

                'quantity':
                    row[1],

                'order_date':
                    row[2],

                'image':
                    product.image

            })

    return render_template(
        'orders.html',
        orders=orders_data
    )

@app.route('/buy_now/<int:product_id>')
def buy_now(product_id):

    if 'user_id' not in session:

        return redirect('/login')

    user_id = session['user_id']

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        INSERT INTO orders(
            user_id,
            product_id,
            quantity
        )

        VALUES(%s,%s,%s)
        ''',
        (
            user_id,
            product_id,
            1
        )
    )

    mysql.connection.commit()

    cursor.close()

    return render_template(
        'order_success.html'
    )

def format_chatbot_products(results, intent=None):

    reply = ""

    # -----------------------------------------
    # RECOMMENDATION EXPLANATION
    # -----------------------------------------

    reasons = []

    if intent:

        if intent.get("occasion") == "college":
            reasons.append("🎓 Suitable for college")

        elif intent.get("occasion") == "office":
            reasons.append("💼 Suitable for office")

        elif intent.get("occasion") == "travel":
            reasons.append("✈️ Great for travel")

        elif intent.get("occasion") == "gift":
            reasons.append("🎁 Good gift options")

        elif intent.get("occasion") == "style_match":
            reasons.append("👗 Matches your style request")

        elif intent.get("occasion") == "walking":
            reasons.append("🚶 Comfortable for walking")

        elif intent.get("occasion") == "trekking":
            reasons.append("🥾 Suitable for trekking")

        elif intent.get("occasion") == "gym":
            reasons.append("🏋️ Great for workouts")

        if intent.get("budget"):
            reasons.append(
                f"💰 Within your budget (₹{intent['budget']})"
            )

        if intent.get("gender") == "women":
            reasons.append("👩 Selected for women")

        elif intent.get("gender") == "men":
            reasons.append("👨 Selected for men")

        elif intent.get("gender") == "kids":
            reasons.append("🧒 Selected for kids")

    reasons.append("⭐ Highly rated products")

    if reasons:

        reply += """
        <div style="
            background:#eef7ff;
            border-left:4px solid #2196F3;
            padding:12px;
            margin-bottom:20px;
            border-radius:6px;
        ">

        <b>🎯 Why these products?</b><br><br>
        """

        for reason in reasons:
            reply += f"✓ {reason}<br>"

        reply += "</div>"

    # -----------------------------------------
    # PRODUCTS
    # -----------------------------------------

    for _, product in results.iterrows():

        reply += f"""
        <div style='margin-bottom:15px;'>

            <img
                src="/static/{product['image']}"
                width="80"
                height="80"
                style="border-radius:5px;"
                onerror="this.src='/static/images/no_image.jpg';"
            >

            <br><br>

            ⭐ <b>{product["product_name"]}</b>

            <br>

            💰 ₹{product["price"]}

            <br>

            ⭐ Rating: {product["rating"]}

            <br><br>

            <a
                href="/recommend/{product['product_id']}"
                style="
                    background:#ff9900;
                    color:white;
                    padding:6px 12px;
                    text-decoration:none;
                    border-radius:5px;
                    display:inline-block;
                "
            >
                View Product
            </a>

        </div>
        """

    return reply

@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()

    message = data.get(
        "message",
        ""
    ).strip()

    query_type = route_query(message)

    if query_type == "personalized":
        return handle_personalized(mysql)

    # -----------------------------
    # FAQ
    # -----------------------------

    if query_type == "faq":

        reply = get_faq_response(message)

        if reply:
            return jsonify({
                "reply": reply
            })

    print("=" * 60)
    print("USER MESSAGE :", message)
    print("QUERY TYPE   :", query_type)
    print("=" * 60)

    # -----------------------------
    # COMBO RECOMMENDATIONS
    # -----------------------------

    response = handle_combo(message)

    if response:
        return response

    # Shopping / Recommendation queries
    if query_type in [
        "shopping",
        "recommendation"
    ]:

        # -----------------------------------------
        # EXTRACT SHOPPING INTENT
        # -----------------------------------------

        intent = extract_chatbot_intent(message)

        if (

                intent["category"] is None

                and

                intent["occasion"] is None

        ):
            intent = extract_ai_intent(message)

        print("INTENT =", intent)

        # -----------------------------------------
        # SEARCH PRODUCTS
        # -----------------------------------------

        results = chatbot_search(intent)

        if len(results) > 0:
            return jsonify({
                "reply": format_chatbot_products(results, intent)
            })


    combo_words = [

        "goes with",
        "combo",
        "accessories",
        "pair with",
        "buy with"

    ]

    is_combo_query = any(
        word in message
        for word in combo_words
    )

    # -----------------------------------------
    # GREETING
    # -----------------------------------------

    if query_type == "greeting":
        return jsonify({
            "reply": get_greeting()
        })

    # -----------------------------------------
    # HELP
    # -----------------------------------------

    if query_type == "help":
        return jsonify({
            "reply": get_help()
        })

    # -----------------------------------------
    # GENERAL AI
    # -----------------------------------------

    if query_type == "general_ai":
        reply = get_gemini_response(message)

        return jsonify({
            "reply": reply
        })

    # -----------------------------
    # CHAT MEMORY
    # -----------------------------

    if any(word in message for word in [
        "backpack",
        "backpacks"
    ]):
        session['chat_category'] = "backpack"

    elif any(word in message for word in [
        "bag",
        "bags"
    ]):
        session['chat_category'] = "bag"

    elif any(word in message for word in [
        "shoe",
        "shoes",
        "sandal",
        "sandals",
        "footwear"
    ]):
        session['chat_category'] = "footwear"

    elif any(word in message for word in [

        "watch",
        "watches"

    ]):


        session['chat_category'] = "watch"

    # If user gives short follow-up reply
    elif (
            len(message.split()) <= 2
            and 'chat_category' in session
    ):
        message = (
                message
                + " "
                + session['chat_category']
        )

    print("FINAL MESSAGE =", message)

    # GEMINI SHOPPING INTENT

    shopping_keywords = [

        "bag",
        "bags",
        "backpack",
        "backpacks",
        "shoe",
        "shoes",
        "sandal",
        "sandals",
        "watch",
        "watches",
        "kurta",
        "dress",
        "jeans",
        "shirt",
        "wallet",
        "belt",
        "jewellery",
        "perfume",
        "lipstick"

    ]

    is_shopping_query = any(
        keyword in message
        for keyword in shopping_keywords
    )

    if is_shopping_query:
        message = "recommend " + message

        print("FORCED RECOMMEND QUERY =", message)

    print("USER MESSAGE =", message)

    # -----------------------------
    # FOLLOW-UP INTENT HANDLING
    # -----------------------------

    # -----------------------------
    # FOLLOW-UP INTENT HANDLING
    # -----------------------------

    if "chat_category" in session:

        followup_words = [

            "travel",
            "weekend getaway",
            "sleek",
            "modern",
            "sleek/modern",
            "stylish",
            "fashionable",
            "college",
            "office",
            "casual"

        ]

        if message.lower().strip() in followup_words:

            message = (
                    message +
                    " " +
                    session["chat_category"]
            )

        else:
            session.pop("chat_category", None)

            print(
                "FOLLOWUP MESSAGE =",
                message
            )

    def extract_product_keyword(message):

        stop_words = [

            "recommend",
            "suggest",
            "need",
            "show",
            "looking",
            "for",
            "me",
            "a",
            "an",
            "the",
            "office",
            "college",
            "daily",
            "casual",
            "stylish",
            "fashionable"

        ]

        words = message.lower().split()

        filtered = [

            word
            for word in words
            if word not in stop_words

        ]

        return " ".join(filtered)

    print("USER MESSAGE =", message)

    # -----------------------------
    # PERSONALIZED RECOMMENDATIONS
    # -----------------------------

    if query_type == "orders":
        return handle_orders(mysql)



    response = handle_deals(message)

    if response:
        return response

    # -----------------------------
    # GREETINGS
    # -----------------------------

    response = handle_greeting(message)

    if response:
        return response

    # -----------------------------
    # HELP
    # -----------------------------

    response = handle_help(message)

    if response:
        return response


    # -----------------------------
    # RECOMMEND PRODUCTS
    # -----------------------------


    if any(word in message for word in [

        "recommend",
        "suggest",
        "need",
        "looking for",
        "show me"

    ]):
        print(products_df['category'].value_counts().head(20))

        intent = extract_chatbot_intent(message)
        print(intent)

        results = chatbot_search(intent)

        print("RESULT COUNT =", len(results))

        if not results.empty:
            return jsonify({
                "reply": format_chatbot_products(results, intent)
            })

        return jsonify({
            "reply":
                "Sorry, I couldn't find matching products for that request."
        })

    message = message.replace("fashionable", "")
    message = message.replace("stylish", "")
    message = message.replace("modern", "")
    message = message.replace("sleek", "")
    message = message.strip()


    # -----------------------------
    # CLEAN QUERY
    # -----------------------------

    message = (
        message
        .replace("fashionable", "")
        .replace("stylish", "")
        .replace("modern", "")
        .replace("sleek", "")
        .replace("casual", "")
    )

    message = " ".join(message.split())

    keywords = [
        "show",
        "find",
        "search",
        "products",
        "product"
    ]

    for word in keywords:
        message = message.replace(
            word,
            ""
        )

    message = message.strip()
    print("AFTER CLEAN =", message)

    # -----------------------------
    # PRODUCT INTENT DETECTION
    # -----------------------------

    if "backpack" in message and "under" not in message:
        message = "backpack"

    elif "watch" in message and "under" not in message:
        message = "watch"

    elif "footwear" in message and "under" not in message:
        message = "sandals"

    elif "shoe" in message and "under" not in message:
        message = "shoes"

    elif "sandal" in message and "under" not in message:
        message = "sandals"

    search_category = None

    if "sandal" in message:
        search_category = "footwear"

    elif "shoe" in message:
        search_category = "footwear"

    elif "watch" in message:
        search_category = "watches"

    elif "bag" in message:
        search_category = "bags, wallets & belts"

    elif "backpack" in message:
        search_category = "bags, wallets & belts"



    elif "bag" in message and "under" not in message:
        message = "bags"

    print("INTENT SEARCH =", message)

    # -----------------------------
    # PRICE FILTER
    # -----------------------------

    if "under" in message:

        parts = message.split("under")

        search_term = parts[0].strip()

        try:

            max_price = int(
                parts[1].strip()
            )

            results = products_df[
                products_df['price']
                <= max_price
            ]

            if search_term != "":

                results = results[

                    results['product_name']
                    .str.lower()
                    .str.contains(
                        search_term,
                        na=False
                    )

                    |

                    results['category']
                    .str.lower()
                    .str.contains(
                        search_term,
                        na=False
                    )

                    |

                    results['subcategory']
                    .str.lower()
                    .str.contains(
                        search_term,
                        na=False
                    )

                ]

            results = results.head(5)

        except:

            results = []

    else:

        results = products_df[

            products_df['combined_features']
            .fillna('')
            .str.lower()
            .str.contains(
                message,
                na=False
            )

            |

            products_df['product_name']
            .fillna('')
            .str.lower()
            .str.contains(
                message,
                na=False
            )

            ]

        if search_category:
            results = results[

                results['category']
                .fillna('')
                .str.lower()
                .str.contains(
                    search_category.lower(),
                    na=False
                )

            ]

        results = results.sort_values(
            by='rating',
            ascending=False
        ).head(5)

    # -----------------------------
    # RESPONSE
    # -----------------------------
    print(
        "RESULT COUNT =",
        len(results)
    )

    if len(results) > 0:

        results = results.head(5)

        reply = ""

        print("FINAL RESULTS =", len(results))

        for _, product in results.iterrows():
            reply += f"""
            <div style='margin-bottom:15px;'>

                <img
                    src="/static/{product['image']}"
                    width="80"
                    height="80"
                    style="border-radius:5px;"
                    onerror="this.src='/static/images/no_image.jpg';"
                >

                <br><br>

                ⭐ {product["product_name"]}

                <br>

                💰 ₹{product["price"]}

                <br>

                ⭐ Rating: {product["rating"]}

                <br><br>

                <a
                    href='/recommend/{product["product_id"]}'
                    style='
                        background:#ff9900;
                        color:white;
                        padding:6px 12px;
                        text-decoration:none;
                        border-radius:5px;
                        display:inline-block;
                    '
                >
                    View Product
                </a>

            </div>
            """

        return jsonify({
            'reply': reply
        })
    else:

        shopping_words = [

            "backpack",
            "bag",
            "bags",
            "shoe",
            "shoes",
            "watch",
            "watches",
            "kurta",
            "dress",
            "shirt",
            "jeans",
            "wallet",
            "belt"

        ]

        if any(
                word in message
                for word in shopping_words
        ):

            reply = "Sorry, no matching products found in our catalog."

        else:

            try:

                response = gemini_model.generate_content(
                    f"""
                    You are a shopping assistant.

                    Extract the main shopping keyword from the user query.

                    Examples:

                    "I need a stylish office bag"
                    → bag

                    "Suggest comfortable footwear for college"
                    → footwear

                    "Show me watches for men"
                    → watch

                    "Recommend a gift handbag"
                    → handbag

                    Return ONLY the keyword.

                    User Query:
                    {message}
                    """
                )

                keyword = (
                    response.text
                    .strip()
                    .lower()
                    .replace('"', '')
                    .replace("'", '')
                )

                keyword = keyword.split('\n')[0]

                keyword = keyword[:50]
                print("GEMINI RAW RESPONSE =", response.text)
                print("GEMINI KEYWORD =", keyword)

                if "watch" in message:
                    keyword = "watch"

                elif "bag" in message:
                    keyword = "bag"

                elif "backpack" in message:
                    keyword = "backpack"

                elif "shoe" in message:
                    keyword = "shoe"

                elif "footwear" in message:
                    keyword = "footwear"

                elif "sandal" in message:
                    keyword = "sandal"

                gemini_results = products_df[

                    products_df['combined_features']
                    .fillna('')
                    .str.lower()
                    .str.contains(
                        keyword,
                        na=False
                    )

                    |

                    products_df['product_name']
                    .fillna('')
                    .str.lower()
                    .str.contains(
                        keyword,
                        na=False
                    )

                    ]

                if len(gemini_results) > 0:

                    gemini_results = (
                        gemini_results
                        .sort_values(
                            by='rating',
                            ascending=False
                        )
                        .head(5)
                    )

                    reply = "<b>Suggested Products:</b><br><br>"

                    for _, product in gemini_results.iterrows():
                        reply += f"""
                        <div style='margin-bottom:15px;'>

                            <img
                                src="/static/{product['image']}"
                                width="80"
                                height="80"
                                style="border-radius:5px;"
                                onerror="this.src='/static/images/no_image.jpg';"
                            >

                            <br><br>

                            ⭐ {product['product_name']}

                            <br>

                            💰 ₹{product['price']}

                            <br>

                            ⭐ Rating: {product['rating']}

                            <br><br>

                            <a
                                href='/recommend/{product["product_id"]}'
                                style='
                                    background:#ff9900;
                                    color:white;
                                    padding:6px 12px;
                                    text-decoration:none;
                                    border-radius:5px;
                                    display:inline-block;
                                '
                            >
                                View Product
                            </a>

                        </div>
                        """

                else:

                    reply = (
                        "Sorry, I couldn't find matching products."
                    )



            except Exception:

                reply = (
                    "Sorry, AI assistant is currently unavailable."
                )

        return jsonify({
            "reply": reply
        })

@app.route('/submit_review/<int:product_id>', methods=['POST'])
def submit_review(product_id):

    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']

    rating = int(request.form['rating'])

    review_text = request.form['review_text']

    cursor = mysql.connection.cursor()

    # Check if review already exists

    cursor.execute(
        '''
        SELECT review_id
        FROM product_reviews
        WHERE user_id=%s
        AND product_id=%s
        ''',
        (
            user_id,
            product_id
        )
    )

    existing_review = cursor.fetchone()

    if existing_review:

        cursor.execute(
            '''
            UPDATE product_reviews
            SET rating=%s,
                review_text=%s
            WHERE user_id=%s
            AND product_id=%s
            ''',
            (
                rating,
                review_text,
                user_id,
                product_id
            )
        )

    else:

        cursor.execute(
            '''
            INSERT INTO product_reviews
            (
                user_id,
                product_id,
                rating,
                review_text
            )

            VALUES (%s,%s,%s,%s)
            ''',
            (
                user_id,
                product_id,
                rating,
                review_text
            )
        )

    mysql.connection.commit()

    cursor.close()

    return redirect(
        url_for(
            'recommend',
            product_id=product_id
        )
    )
# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )

