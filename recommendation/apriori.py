import pickle
from pathlib import Path

from recommendation.model import products_df

# -----------------------------------
# LOAD PRE-BUILT APRIORI RULES
# -----------------------------------

MODEL_PATH = Path(__file__).parent / "apriori_rules.pkl"

with open(MODEL_PATH, "rb") as f:

    rules_filtered = pickle.load(f)

print(f"Loaded {len(rules_filtered)} Apriori rules.")


# -----------------------------------
# APRIORI RECOMMENDATIONS
# -----------------------------------

def get_apriori_recommendations(product_id, top_n=15):
    print("\nPRODUCT ID =", product_id)
    print("PRODUCT TYPE =", type(product_id))

    relevant_rules = [

        rule

        for rule in rules_filtered

        if product_id in rule["antecedents"]

    ]

    print("\n==========================")
    print("CURRENT PRODUCT ID :", product_id)
    print("MATCHING RULES :", len(relevant_rules))
    print("==========================\n")

    if not relevant_rules:
        return []

    current = products_df[
        products_df["product_id"] == product_id
    ]

    if current.empty:
        return []

    current = current.iloc[0]

    current_category = str(current["category"]).strip().lower()
    current_gender = str(current["gender_feature"]).strip().lower()
    current_type = str(current["type_feature"]).strip().lower()

    scored_products = {}

    for rule in relevant_rules:

        confidence = rule["confidence"]
        lift = rule["lift"]

        for pid in rule["consequents"]:

            product = products_df[
                products_df["product_id"] == pid
            ]

            if product.empty:
                continue

            product = product.iloc[0]

            score = confidence * 100
            score += lift * 20

            if str(product["category"]).strip().lower() == current_category:
                score += 40

            if str(product["gender_feature"]).strip().lower() == current_gender:
                score += 30

            if str(product["type_feature"]).strip().lower() != current_type:
                score += 20

            score += float(product["rating"]) * 10

            scored_products[pid] = max(
                score,
                scored_products.get(pid, 0)
            )

    ranked = sorted(
        scored_products.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        pid
        for pid, _ in ranked[:top_n]
    ]