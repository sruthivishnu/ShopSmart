from flask import jsonify

from recommendation.chatbot_intent import (
    extract_chatbot_intent
)

from recommendation.chatbot_ai import (
    extract_ai_intent
)

from recommendation.chatbot_search import (
    chatbot_search
)

def handle_shopping(message, query_type, formatter):

    if query_type not in [
        "shopping",
        "recommendation"
    ]:
        return None

    intent = extract_chatbot_intent(message)

    if (

        intent["category"] is None

        and

        intent["occasion"] is None

    ):

        intent = extract_ai_intent(message)

    print("INTENT =", intent)

    results = chatbot_search(intent)

    if len(results) > 0:

        return jsonify({

            "reply":

            formatter(
                results,
                intent
            )

        })

    return None