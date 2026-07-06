import re


def route_query(message):

    """
    Decide what type of query the user is asking.

    Returns one of:

    greeting
    help
    shopping
    recommendation
    personalized
    orders
    deals
    trending
    faq
    general_ai
    """

    message = message.lower().strip()

    # -----------------------------
    # GREETING
    # -----------------------------

    if message in [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]:
        return "greeting"

    # -----------------------------
    # HELP
    # -----------------------------

    if "help" in message:
        return "help"

    # -----------------------------
    # PERSONALIZED
    # -----------------------------

    if any(text in message for text in [

        "recommend for me",
        "what should i buy",
        "suggest products for me",
        "recommend products for me"

    ]):

        return "personalized"

    # -----------------------------
    # ORDERS
    # -----------------------------

    if any(text in message for text in [

        "my orders",
        "recent purchases",
        "buy again",
        "what did i buy"

    ]):

        return "orders"

    # -----------------------------
    # DEALS
    # -----------------------------

    if any(text in message for text in [

        "today's deals",
        "todays deals",
        "offers",
        "discount",
        "best offers"

    ]):

        return "deals"

    # -----------------------------
    # TRENDING
    # -----------------------------

    if any(text in message for text in [

        "trending",
        "hot picks",
        "what's trending",
        "whats trending"

    ]):

        return "trending"

    # -----------------------------
    # RECOMMENDATION
    # -----------------------------

    if any(text in message for text in [

        "goes with",
        "pair with",
        "buy with",
        "combo",
        "accessories",
        "match with",
        "what matches",
        "wear with"

    ]):

        return "recommendation"

    # -----------------------------
    # SHOPPING
    # -----------------------------

    shopping_keywords = [

        # Shopping verbs
        "recommend",
        "suggest",
        "show",
        "need",
        "looking for",
        "find",

        # Follow-up conversation
        "for",
        "under",
        "below",
        "less than",
        "maximum",
        "around",
        "between",

        # Product categories
        "shoe",
        "shoes",
        "sandal",
        "sandals",
        "heels",
        "watch",
        "watches",
        "bag",
        "bags",
        "wallet",
        "wallets",
        "backpack",
        "backpacks",

        "shirt",
        "dress",
        "jeans",
        "kurta",
        "kurti",
        "top",
        "tops",

        "chair",
        "table",
        "sofa",

        "perfume",
        "lipstick",
        "cream",

        # Gender
        "men",
        "women",
        "kids",

        # Occasions
        "office",
        "college",
        "travel",
        "party",
        "gift",
        "birthday",
        "interview",
        "walking",
        "gym",
        "trekking",
        "vacation",

        # Shopping adjectives
        "comfortable",
        "casual",
        "formal",
        "premium",
        "budget",
        "affordable",
        "cheap",
        "luxury",

        # Colours
        "black",
        "white",
        "blue",
        "red"

    ]

    if any(word in message for word in shopping_keywords):
        return "shopping"

    # Very short follow-up messages
    # should continue shopping conversation

    if len(message.split()) <= 3:
        return "shopping"

    # -----------------------------
    # FAQ
    # -----------------------------

    faq_words = [

        "return",
        "refund",
        "replace",
        "exchange",

        "delivery",
        "shipping",
        "payment",

        "cancel order",

        "cash on delivery",
        "cod"

    ]

    if any(word in message for word in faq_words):

        return "faq"

    # -----------------------------
    # GENERAL AI
    # -----------------------------

    # -----------------------------
    # GENERAL AI
    # -----------------------------

    general_ai_keywords = [

        "what is",
        "what's",
        "explain",
        "difference between",
        "compare",
        "how does",
        "how do",
        "why",
        "technology",
        "ai",
        "artificial intelligence",
        "bluetooth",
        "wifi",
        "wi-fi",
        "usb",
        "usb-c",
        "ssd",
        "hdd",
        "oled",
        "amoled",
        "lcd",
        "processor",
        "ram"

    ]

    if any(keyword in message for keyword in general_ai_keywords):
        return "general_ai"

    return "general_ai"