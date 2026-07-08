import joblib
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from recommendation.product_intelligence import (
    detect_gender,
    detect_product_type,
    build_combined_features,
    get_canonical_category
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

products_path = os.path.join(
    BASE_DIR,
    "products_cleaned.csv"
)

products_df = pd.read_csv(products_path)

products_df.fillna("", inplace=True)

products_df["category"] = (
    products_df["category"]
    .astype(str)
    .str.lower()
)

products_df["gender_feature"] = (
    products_df["product_name"]
    .apply(detect_gender)
)

products_df["type_feature"] = (
    products_df["product_name"]
    .apply(detect_product_type)
)

products_df["canonical_category"] = (
    products_df.apply(
        lambda row: get_canonical_category(
            row["type_feature"],
            row["category"]
        ),
        axis=1
    )
)

products_df["combined_features"] = (
    products_df.apply(
        build_combined_features,
        axis=1
    )
)

vectorizer = TfidfVectorizer(
    stop_words="english"
)

feature_vectors = vectorizer.fit_transform(
    products_df["combined_features"]
)

joblib.dump(
    vectorizer,
    "tfidf_vectorizer.pkl"
)

joblib.dump(
    feature_vectors,
    "feature_vectors.pkl"
)

print("TF-IDF model saved successfully.")