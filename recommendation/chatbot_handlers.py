from flask import jsonify, session

from recommendation.model import products_df
from recommendation.user_recommendation import (
    get_user_recommendations
)


def handle_personalized(mysql):

    if 'user_id' not in session:

        return jsonify({
            "reply":
                "Please login first to get personalized recommendations."
        })

    recommendations = get_user_recommendations(
        session['user_id'],
        mysql
    )

    if not recommendations:

        return jsonify({
            "reply":
                "I don't have enough purchase history yet."
        })

    reply = "<b>Recommended For You:</b><br><br>"

    for product in recommendations[:5]:

        reply += f"""
        ⭐ {product['product_name']}<br>
        💰 ₹{product['price']}<br>
        ⭐ {product['rating']}<br><br>

        <a href="/recommend/{product['product_id']}">
            View Product
        </a>

        <br><br>
        """

    return jsonify({
        "reply": reply
    })



def handle_orders(mysql):

    if 'user_id' not in session:
        return jsonify({
            "reply":
                "Please login first to view your purchase history."
        })

    cursor = mysql.connection.cursor()

    cursor.execute(
        '''
        SELECT product_id
        FROM orders
        WHERE user_id=%s
        ORDER BY order_date DESC
        LIMIT 5
        ''',
        (session['user_id'],)
    )

    rows = cursor.fetchall()

    cursor.close()

    if not rows:
        return jsonify({
            "reply":
                "You haven't purchased any products yet."
        })

    reply = "<b>Your Recent Purchases:</b><br><br>"

    for row in rows:

        product_id = row[0]

        product = products_df[
            products_df['product_id'] == product_id
        ]

        if product.empty:
            continue

        product = product.iloc[0]

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
        "reply": reply
    })


def handle_deals(message):
    """
    Handles deal/offer related chatbot requests.
    Returns:
        Flask jsonify(...) response if handled,
        otherwise None.
    """

    message = message.lower().strip()

    # -----------------------------
    # DEALS & TRENDING
    # -----------------------------

    if any(text in message for text in [

        "today's deals",
        "todays deals",
        "show deals",
        "best offers",
        "offers"

    ]):

        deals = (

            products_df[

                (products_df['price'] < 2000)

                &

                products_df['product_name']
                .str.contains(
                    r'dress|kurta|jeans|watch|shoe|sandal|bag|perfume|lipstick',
                    case=False,
                    na=False,
                    regex=True
                )

                ]

                .sort_values(
                by='rating',
                ascending=False
            )

                .drop_duplicates(
                subset='product_name'
            )

                .head(5)

        )

        reply = "<b>🔥 Today's Deals</b><br><br>"

        for _, product in deals.iterrows():
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

        return jsonify({
            "reply": reply
        })

    if any(text in message for text in [

        "trending products",
        "what's trending",
        "whats trending",
        "hot picks",
        "trending"

    ]):

        trending = (

            products_df[

                products_df['product_name']
                .str.contains(
                    r'dress|kurta|jeans|watch|shoe|sneaker|heel|bag|handbag|backpack',
                    case=False,
                    na=False,
                    regex=True
                )

            ]

                .sort_values(
                by='rating',
                ascending=False
            )

                .drop_duplicates(
                subset='product_name'
            )

                .head(5)

        )

        reply = "<b>🔥 Hot Picks</b><br><br>"

        for _, product in trending.iterrows():
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

        return jsonify({
            "reply": reply
        })

    return None

def handle_greeting(message):

    message = message.lower().strip()

    if message in [

        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"

    ]:

        return jsonify({

            "reply":
            '''
            👋 Hello!

            <br><br>

            I can help you find products.

            <br><br>

            Try:

            <br>

            🛍️ bags

            <br>

            🛍️ sandals

            <br>

            💰 products under 5000

            <br>

            💰 bags under 3000

            <br>

            ⭐ recommend bags
            '''

        })

    return None

def handle_help(message):

    message = message.lower().strip()

    if "help" in message:

        return jsonify({

            "reply":
            '''
            📋 Available Commands

            <br><br>

            🛍️ show bags

            <br>

            🛍️ show sandals

            <br>

            🛍️ show kitchen

            <br>

            💰 products under 5000

            <br>

            💰 bags under 3000

            <br>

            💰 sandals under 2000

            <br>

            ⭐ recommend bags

            <br>

            ⭐ recommend sandals
            '''

        })

    return None