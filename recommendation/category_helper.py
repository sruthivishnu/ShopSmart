from flask import render_template, url_for

from recommendation.subcategory_images import (
    SUBCATEGORY_IMAGES,
    IMAGE_MAP
)

from recommendation.category_subtypes import CATEGORY_SUBTYPES


def build_subcategory_page(
        category_name,
        display_name,
        products,
        hero_image
):

    # -------------------------
    # Build subcategories
    # -------------------------

    # -------------------------------------
    # FASHION
    # -------------------------------------

    if category_name in ["men", "women", "kids"]:

        subcategories = (

            products["type_feature"]

            .value_counts()

            .reset_index()

        )

        subcategories.columns = [

            "type",

            "count"

        ]

        subcategories = subcategories.to_dict("records")

    # -------------------------------------
    # OTHER CATEGORIES
    # -------------------------------------

    else:

        subcategories = []

        mapping = CATEGORY_SUBTYPES.get(

            category_name,

            {}

        )

        for subtype, keywords in mapping.items():

            mask = False

            for word in keywords:
                mask = (

                        mask

                        |

                        products["product_name"]

                        .str.contains(

                            word,

                            case=False,

                            na=False,

                            regex=False

                        )

                )

            count = products[mask].shape[0]

            if count > 0:
                subcategories.append({

                    "type": subtype,

                    "count": count

                })

    

    # -------------------------
    # Assign Images
    # -------------------------

    for item in subcategories:

        product_type = item["type"]

        image = SUBCATEGORY_IMAGES.get(
            product_type,
            "default.jpg"
        )

        if category_name in IMAGE_MAP:

            image = IMAGE_MAP[category_name].get(
                product_type,
                image
            )

        item["image"] = image

    hero_image = url_for(
        "static",
        filename=hero_image
    )

    return render_template(

        "subcategory.html",

        category_name=display_name,

        gender=category_name,

        subcategories=subcategories,

        hero_image=hero_image

    )