from recommendation.model import products_df

def category_based_recommendation(product_id, top_n=10):

    category = products_df.loc[
        products_df['product_id'] == product_id,
        'category'
    ].values[0]

    recommendations = products_df[
        products_df['category'] == category
    ]

    recommendations = recommendations[
        recommendations['product_id'] != product_id
    ]

    return recommendations.head(top_n)