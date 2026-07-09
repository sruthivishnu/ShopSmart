from flask import jsonify

from recommendation.model import products_df

from recommendation.apriori import (
    get_apriori_recommendations
)


def handle_combo(message):

    message = message.lower().strip()

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
    

    if not is_combo_query:
        return None

    # -----------------------------
    # COMBO RECOMMENDATIONS (APRIORI)
    # -----------------------------

    if is_combo_query:

        combo_keyword = None

        if "backpack" in message:
            combo_keyword = "backpack"

            print("COMBO KEYWORD =", combo_keyword)

        elif "watch" in message:
            combo_keyword = "watch"

        elif "shoe" in message:
            combo_keyword = "shoe"

        elif "sandal" in message:
            combo_keyword = "sandal"

        elif "heel" in message:
            combo_keyword = "heel"

        elif "wedge" in message:
            combo_keyword = "wedge"

        elif "bag" in message:
            combo_keyword = "bag"

        if not combo_keyword:
            return jsonify({
                "reply":
                    "Please specify a product. Example: 'What goes with heels?'"
            })

        # Find a matching product

        base_products = products_df[

            products_df['product_name']
            .fillna('')
            .str.contains(
                combo_keyword,
                case=False,
                na=False
            )

        ]

        if base_products.empty:
            return jsonify({
                "reply":
                    f"I couldn't find any {combo_keyword} products."
            })

        base_product = base_products.iloc[0]

        product_id = int(
            base_product['product_id']
        )

        recommended_ids = get_apriori_recommendations(
            product_id,
            top_n=5
        )

        if not recommended_ids:

            category_map = {

                'footwear': [
                    'bags, wallets & belts',
                    'watches',
                    'jewellery',
                    'clothing'
                ],

                'clothing': [
                    'footwear',
                    'bags, wallets & belts',
                    'watches'
                ],

                'bags, wallets & belts': [
                    'footwear',
                    'clothing',
                    'watches'
                ],

                'watches': [
                    'bags, wallets & belts',
                    'footwear',
                    'clothing'
                ]
            }

            current_category = str(
                base_product['category']
            ).strip().lower()

            target_categories = category_map.get(
                current_category,
                [current_category]
            )

            recommendations = products_df[

                products_df['category']
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(target_categories)

            ].copy()

            # Remove products without real images

            recommendations = recommendations[

                recommendations['image']
                .notna()

                &

                (~recommendations['image']
                 .str.contains(
                    'default.jpg',
                    case=False,
                    na=False
                ))
                ]

            # Remove the base product

            recommendations = recommendations[
                recommendations['product_id'] != product_id
                ]

            # Highest rated first

            recommendations = recommendations.sort_values(
                by='rating',
                ascending=False
            )

            recommendations = recommendations.drop_duplicates(
                subset='type_feature'
            )

            recommendations = recommendations.head(5)

            recommendations = recommendations[

                recommendations['product_id']
                != product_id

                ]

            recommendations = recommendations.sort_values(
                by='rating',
                ascending=False
            ).head(5)

        else:

            recommendations = products_df[

                products_df['product_id']
                .isin(recommended_ids)

            ]

        reply = f"""
        <b>Frequently Bought Together with {combo_keyword.title()}:</b>
        <br><br>
        """

        print(
            "FINAL DISPLAY COUNT =",
            len(recommendations)
        )

        for _, product in recommendations.iterrows():
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