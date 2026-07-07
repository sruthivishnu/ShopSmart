import pickle
from pathlib import Path

from mlxtend.frequent_patterns import apriori, association_rules

import pandas as pd

print("Building Apriori Model...")

# -----------------------------------
# LOAD TRANSACTIONS
# -----------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

transactions_df = pd.read_csv(
    BASE_DIR / "transactions.csv"
)

print("Transactions :", len(transactions_df))

# -----------------------------------
# REMOVE VERY RARE PRODUCTS
# -----------------------------------

product_counts = (
    transactions_df["product_id"]
    .value_counts()
)

valid_products = product_counts[
    product_counts >= 5
].index

transactions_df = transactions_df[
    transactions_df["product_id"]
    .isin(valid_products)
]

print("Products Used :", len(valid_products))

# -----------------------------------
# CREATE MEMORY-EFFICIENT BASKET
# -----------------------------------

transactions_df["value"] = True

basket = transactions_df.pivot_table(

    index="transaction_id",

    columns="product_id",

    values="value",

    aggfunc="max",

    fill_value=False

)

basket = basket.astype(bool)

print("Basket Shape :", basket.shape)

# -----------------------------------
# FREQUENT ITEMSETS
# -----------------------------------

frequent_items = apriori(
    basket,
    min_support=0.0001,
    use_colnames=True,
    low_memory=True
)

print("Frequent Itemsets:", len(frequent_items))

# -----------------------------------
# ASSOCIATION RULES
# -----------------------------------

rules = association_rules(
    frequent_items,
    metric="lift",
    min_threshold=0.1
)

rules_filtered = rules[
    (rules["confidence"] >= 0.30) &
    (rules["lift"] >= 1.20)
].copy()

print("Filtered Rules:", len(rules_filtered))

# -----------------------------------
# SAVE MODEL (Portable Format)
# -----------------------------------

MODEL_PATH = Path(__file__).resolve().parent / "apriori_rules.pkl"

portable_rules = []

for _, row in rules_filtered.iterrows():

    portable_rules.append({

        "antecedents": list(row["antecedents"]),

        "consequents": list(row["consequents"]),

        "confidence": float(row["confidence"]),

        "lift": float(row["lift"])

    })

with open(MODEL_PATH, "wb") as f:

    pickle.dump(portable_rules, f)

print(f"Apriori model saved successfully: {MODEL_PATH}")

# -----------------------------------
# STATISTICS
# -----------------------------------

all_products = set()

for _, rule in rules_filtered.iterrows():
    all_products.update(rule["antecedents"])
    all_products.update(rule["consequents"])

print("Products covered:", len(all_products))