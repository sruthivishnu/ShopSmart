import os
from pathlib import Path

import pandas as pd
import pymysql
from dotenv import load_dotenv

print("=" * 60)
print("SHOPSMART APRIORI RETRAINING")
print("=" * 60)

# -----------------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# CONNECT TO MYSQL
# -----------------------------------

connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DB")
)

print("✓ Connected to MySQL")

# -----------------------------------
# LOAD HISTORICAL TRANSACTIONS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent

historical_df = pd.read_csv(
    BASE_DIR / "transactions.csv"
)

print(f"Historical Transactions : {len(historical_df)}")

# -----------------------------------
# LOAD LIVE ORDERS
# -----------------------------------

query = """
SELECT
    transaction_id,
    product_id
FROM orders
WHERE transaction_id IS NOT NULL
"""

mysql_df = pd.read_sql(query, connection)

connection.close()

print(f"Live Transactions : {len(mysql_df)}")

# -----------------------------------
# MATCH DATA TYPES
# -----------------------------------

historical_df["transaction_id"] = historical_df["transaction_id"].astype(str)
mysql_df["transaction_id"] = mysql_df["transaction_id"].astype(str)

# -----------------------------------
# MERGE HISTORICAL + LIVE DATA
# -----------------------------------

transactions_df = pd.concat(
    [historical_df, mysql_df],
    ignore_index=True
)

print(f"Combined Transactions : {len(transactions_df)}")

import pickle
from mlxtend.frequent_patterns import apriori, association_rules

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
    transactions_df["product_id"].isin(valid_products)
]

print(f"Products Used : {len(valid_products)}")

# -----------------------------------
# CREATE BASKET
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

print(f"Basket Shape : {basket.shape}")

# -----------------------------------
# FREQUENT ITEMSETS
# -----------------------------------

frequent_items = apriori(
    basket,
    min_support=0.0001,
    use_colnames=True,
    low_memory=True
)

print(f"Frequent Itemsets : {len(frequent_items)}")

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

print(f"Filtered Rules : {len(rules_filtered)}")

# -----------------------------------
# CONVERT RULES TO PORTABLE FORMAT
# -----------------------------------

portable_rules = []

for _, row in rules_filtered.iterrows():
    portable_rules.append({
        "antecedents": list(row["antecedents"]),
        "consequents": list(row["consequents"]),
        "confidence": float(row["confidence"]),
        "lift": float(row["lift"]),
        "support": float(row["support"])
    })

print(f"Portable Rules : {len(portable_rules)}")

# -----------------------------------
# SAVE RULES
# -----------------------------------

output_path = BASE_DIR / "recommendation" / "apriori_rules.pkl"

with open(output_path, "wb") as f:
    pickle.dump(portable_rules, f)

print(f"\n✓ Saved {len(portable_rules)} rules")
print(f"Location : {output_path}")

print("\n🎉 Apriori retraining completed successfully!")