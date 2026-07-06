from flask import session

from recommendation.user_recommendation import (
    get_user_recommendations
)


def get_personalized_reply(mysql):

    if "user_id" not in session:

        return None, (
            "🔒 Please log in to get personalized recommendations."
        )

    try:

        products = get_user_recommendations(
            session["user_id"],
            mysql
        )

        if not products:

            return None, (
                "🛍️ Purchase a few products first to receive personalized recommendations."
            )

        return products, None

    except Exception as e:

        print("PERSONALIZED ERROR =", e)

        return None, (
            "Sorry, something went wrong while generating recommendations."
        )