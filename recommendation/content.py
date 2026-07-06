import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from recommendation.model import (
    products_df,
    feature_vectors
)

from sklearn.metrics.pairwise import cosine_similarity

# Combine text
products_df['combined_features'] = (
    products_df['product_name'].fillna('') + ' ' +
    products_df['category'].fillna('') + ' ' +
    products_df['description'].fillna('')
)

def get_content_recommendations(product_id, top_n=20):

    try:
        idx = products_df[
            products_df["product_id"] == product_id
        ].index[0]

    except:
        return pd.DataFrame()

    product_vector = feature_vectors[idx]

    scores = cosine_similarity(
        product_vector,
        feature_vectors
    ).flatten()

    similarity_scores = list(
        enumerate(scores)
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    candidate_indices = [
        i
        for i, score in similarity_scores
        if i != idx
    ]

    recommendations = (
        products_df
        .iloc[candidate_indices]
        .copy()
    )

    # ----------------------------------
    # REMOVE SAME PRODUCT NAME
    # ----------------------------------

    selected_name = (
        products_df.loc[idx, "product_name"]
        .strip()
        .lower()
    )

    recommendations = recommendations[

        recommendations["product_name"]

        .str.lower()

        != selected_name

    ]

    # ----------------------------------
    # REMOVE DUPLICATE PRODUCT NAMES
    # ----------------------------------

    recommendations = recommendations.drop_duplicates(
        subset="product_name"
    )

    return recommendations.head(top_n)
