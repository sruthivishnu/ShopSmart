from recommendation.model import products_df


def get_recently_viewed(user_id, mysql):

    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT product_id
        FROM recently_viewed
        WHERE user_id=%s
        ORDER BY viewed_at DESC
        LIMIT 10
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()

    if not rows:
        return []

    product_ids = []

    seen = set()

    for row in rows:

        pid = row[0]

        if pid not in seen:

            product_ids.append(pid)

            seen.add(pid)

    recent_products = products_df[
        products_df['product_id']
        .isin(product_ids)
    ]

    recent_products = recent_products[

        recent_products['image']
        .notna()

        &

        (~recent_products['image']
          .str.contains(
              'default.jpg',
              case=False,
              na=False
          ))

    ]

    return recent_products.to_dict(
        orient='records'
    )