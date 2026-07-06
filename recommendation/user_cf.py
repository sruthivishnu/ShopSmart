import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from recommendation.model import transactions_df, products_df

# MERGE CATEGORY
cf_df = pd.merge(
    transactions_df,
    products_df[['product_id', 'category']],
    on='product_id',
    how='left'
)
# USER CATEGORY INTERACTION
user_category = (
    cf_df.groupby(['user_id', 'category'])
    .size()
    .reset_index(name='interaction')
)

# MATRIX
user_category_matrix = user_category.pivot_table(
    index='user_id',
    columns='category',
    values='interaction',
    fill_value=0
)
# SIMILARITY
user_similarity = cosine_similarity(user_category_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_category_matrix.index,
    columns=user_category_matrix.index
)
# RECOMMEND CATEGORIES

def recommend_categories(user_id, top_n=5):

    similar_users = user_similarity_df[user_id].sort_values(
        ascending=False
    )[1:11]

    similar_user_ids = similar_users.index

    category_scores = {}

    for sim_user in similar_user_ids:

        categories = user_category[
            user_category['user_id'] == sim_user
        ]
        for _, row in categories.iterrows():

            cat = row['category']

            score = row['interaction']

            if cat not in category_scores:
                category_scores[cat] = 0

            category_scores[cat] += score

    recommended_categories = sorted(
        category_scores,
        key=category_scores.get,
        reverse=True
    )
    return recommended_categories[:top_n]