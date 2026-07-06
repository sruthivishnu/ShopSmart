import random
import pandas as pd

from recommendation.product_intelligence import (
    detect_product_type,
    get_compatible_types
)

# -----------------------------------------
# LOAD PRODUCTS
# -----------------------------------------

products = pd.read_csv("products_fixed.csv")

print("Products Loaded :", len(products))

products["product_name"] = (
    products["product_name"]
    .fillna("")
    .str.lower()
)

products["category"] = (
    products["category"]
    .fillna("")
    .str.lower()
)

# -----------------------------------------
# BUILD PRODUCT LOOKUP
# -----------------------------------------

product_lookup = {}

for _, row in products.iterrows():

    product_lookup[row["product_id"]] = row

print("Product Lookup :", len(product_lookup))

# -----------------------------------------
# BUILD TYPE LOOKUP
# -----------------------------------------

from collections import defaultdict

type_lookup = defaultdict(list)

for _, row in products.iterrows():

    product_type = detect_product_type(
        row["product_name"]
    )

    type_lookup[product_type].append(
        row["product_id"]
    )

print("\nPRODUCT TYPES\n")

for product_type in sorted(type_lookup):

    print(
        f"{product_type:<20}",
        len(type_lookup[product_type])
    )

# -----------------------------------------
# GENERATE TRANSACTIONS
# -----------------------------------------

transactions = []

transaction_id = 1

for _, row in products.iterrows():

    anchor_id = row["product_id"]

    product_type = detect_product_type(
        row["product_name"]
    )

    compatible_types = get_compatible_types(
        product_type
    )

    # Create multiple realistic shopping baskets
    for _ in range(5):

        basket = [anchor_id]

        compatible_types = get_compatible_types(product_type)

        for compatible_type in compatible_types:

            if compatible_type not in type_lookup:
                continue

            candidates = type_lookup[compatible_type]

            if not candidates:
                continue

            # Choose one compatible product
            partner = random.choice(candidates)

            # Avoid duplicates
            if partner != anchor_id and partner not in basket:
                basket.append(partner)

        # Occasionally add one extra accessory
        if random.random() < 0.4:

            extra_candidates = []

            for compatible_type in compatible_types:

                if compatible_type in type_lookup:
                    extra_candidates.extend(type_lookup[compatible_type])

            if extra_candidates:

                extra = random.choice(extra_candidates)

                if extra not in basket and extra != anchor_id:
                    basket.append(extra)

        for pid in basket:

            transactions.append({

                "transaction_id": transaction_id,
                "product_id": pid

            })

        transaction_id += 1
transactions_df = pd.DataFrame(transactions)

print()

print("Transactions Generated :", len(transactions_df))

print("Unique Transactions :", transactions_df["transaction_id"].nunique())

print("Unique Products :", transactions_df["product_id"].nunique())

transactions_df.to_csv(
    "transactions.csv",
    index=False
)

print()

print("transactions.csv created successfully.")