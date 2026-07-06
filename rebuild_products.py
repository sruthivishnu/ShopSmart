import pandas as pd

# ----------------------------------
# LOAD ORIGINAL FLIPKART DATASET
# ----------------------------------

flipkart = pd.read_csv(
    "flipkart_com-ecommerce_sample.csv"
)

print("Original Products :", len(flipkart))

# ----------------------------------
# KEEP REQUIRED COLUMNS
# ----------------------------------

flipkart = flipkart[
    [
        "product_name",
        "product_category_tree",
        "image",
        "description"
    ]
].copy()

print("Columns Loaded:")
print(flipkart.columns.tolist())

# ----------------------------------
# EXTRACT CATEGORY
# ----------------------------------

flipkart["category"] = (

    flipkart["product_category_tree"]

    .fillna("")

    .str.split(">>")

    .str[0]

    .str.replace("[", "", regex=False)

    .str.replace("]", "", regex=False)

    .str.replace('"', "", regex=False)

    .str.strip()

    .str.lower()

)

print("\nFIRST 20 CATEGORIES\n")

print(

    flipkart[

        ["product_name", "category"]

    ].head(20)

)

print("\nUNIQUE CATEGORY COUNT =",

      flipkart["category"].nunique()

)

print("\nCATEGORIES\n")

print(

    sorted(

        flipkart["category"].unique()

    )

)