import pandas as pd

from recommendation.model import products_df


def get_user_recommendations(user_id, mysql):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT product_id
        FROM orders
        WHERE user_id=%s
        ORDER BY order_id DESC
        LIMIT 15
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()

    if not rows:
        return []

    purchased_ids = [
        row[0]
        for row in rows
    ]

    purchased_products = products_df[
        products_df['product_id']
        .isin(purchased_ids)
    ]

    # -----------------------------------
    # TOP TYPE FEATURES
    # -----------------------------------

    if purchased_products.empty:
        return []

    # -----------------------------------
    # RECENT PURCHASE PROFILE
    # -----------------------------------

    recent_categories = (
        purchased_products['category']
        .value_counts()
    )

    print("\nRECENT CATEGORY COUNTS")
    print(recent_categories)

    top_category = recent_categories.index[0]

    print(
        "\nTOP RECENT CATEGORY:",
        top_category
    )


    category_counts = (
        purchased_products['category']
        .value_counts()
    )

    print("\nCATEGORY COUNTS")
    print(category_counts)

    recommendation_frames = []

    top_categories = recent_categories.head(3)

    for category, count in top_categories.items():

        print(f"\nCATEGORY: {category}")

        print("COUNT:", count)

        print("\nPURCHASED PRODUCTS")
        print(
            purchased_products[
                ['product_name', 'category']
            ]
        )

        category_products = products_df[

            (products_df['category'] == category)

            &

            (~products_df['product_id']
             .isin(purchased_ids))

        ]

        # Learn gender from recent purchases
        recent_text = " ".join(

            purchased_products[
                purchased_products['category'] == category
                ]['product_name']

            .fillna('')
            .astype(str)

        ).lower()

        if "women" in recent_text:

            category_products = category_products[
                category_products['product_name']
                .fillna('')
                .str.lower()
                .str.contains(
                    "women|woman|ladies",
                    na=False
                )
            ]

        elif "men" in recent_text:

            category_products = category_products[
                category_products['product_name']
                .fillna('')
                .str.lower()
                .str.contains(
                    "men|man",
                    na=False
                )
            ]

        elif "boy" in recent_text:

            category_products = category_products[
                category_products['product_name']
                .fillna('')
                .str.lower()
                .str.contains(
                    "boy|boys",
                    na=False
                )
            ]

        elif "girl" in recent_text:

            category_products = category_products[
                category_products['product_name']
                .fillna('')
                .str.lower()
                .str.contains(
                    "girl|girls",
                    na=False
                )
            ]

        # Weight recommendations
        if count >= 5:
            n = 8

        elif count >= 2:
            n = 6

        else:
            n = 5

        # -----------------------------------
        # TYPE FEATURE FILTERING
        # -----------------------------------

        print(
            "AVAILABLE PRODUCTS:",
            len(category_products)
        )
        category_products = category_products[

            category_products['image']
            .notna()

            &

            (~category_products['image']
             .str.contains(
                'default.jpg',
                case=False,
                na=False
            ))

        ]

        # -----------------------------------
        # LEARN TYPE PREFERENCE
        # -----------------------------------

        recent_category_products = purchased_products[

            purchased_products['category']
            == category

            ]

        type_counts = {}

        for _, row in recent_category_products.iterrows():

            feature = str(
                row['type_feature']
            ).lower().strip()

            if not feature:
                continue

            main_type = feature.split()[0]

            type_counts[main_type] = (
                    type_counts.get(main_type, 0) + 1
            )

        preferred_types = [

            t

            for t, c in sorted(
                type_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:3]

        ]

        print(
            "\nPREFERRED TYPES:",
            preferred_types
        )

        if preferred_types:

            type_pattern = "|".join(
                preferred_types
            )

            type_matches = category_products[

                category_products[
                    'type_feature'
                ]

                .fillna('')
                .str.lower()

                .str.contains(
                    type_pattern,
                    na=False
                )

            ]

            if len(type_matches) >= n:

                category_products = (
                    type_matches
                    .sort_values(
                        by='rating',
                        ascending=False
                    )
                    .head(n)
                )

            else:

                remaining = n - len(type_matches)

                extra_products = category_products[

                    ~category_products.index.isin(
                        type_matches.index
                    )

                ]

                extra_products = (
                    extra_products
                    .sort_values(
                        by='rating',
                        ascending=False
                    )
                    .head(remaining)
                )

                category_products = pd.concat(
                    [
                        type_matches,
                        extra_products
                    ]
                )

        else:

            category_products = (

                category_products

                .sort_values(
                    by='rating',
                    ascending=False
                )

                .head(n)

            )

        recommendation_frames.append(
            category_products
        )

    if not recommendation_frames:
        return []

    recommendations = pd.concat(
        recommendation_frames
    )

    return recommendations.to_dict(
        orient='records'
    )