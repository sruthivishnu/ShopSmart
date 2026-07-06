from flask import session


# -----------------------------------------
# SAVE LAST SHOPPING INTENT
# -----------------------------------------

def save_chat_intent(intent):

    if not intent:
        return

    session["last_chat_intent"] = intent


# -----------------------------------------
# GET LAST SHOPPING INTENT
# -----------------------------------------

def get_chat_intent():

    return session.get(
        "last_chat_intent",
        {}
    )


# -----------------------------------------
# MERGE PREVIOUS + CURRENT INTENT
# -----------------------------------------
def merge_intents(previous, current):

    if not previous:
        return current

    # -----------------------------------------
    # START A NEW SHOPPING CONVERSATION
    # -----------------------------------------

    if current.get("category"):

        previous_category = previous.get("category")

        previous_type = previous.get("type")

        current_category = current.get("category")

        current_type = current.get("type")

        # Different category → start fresh

        # New product request → start fresh

        if current_category:

            if (
                    current_category != previous_category
                    or
                    (
                            current_type
                            and
                            current_type != previous_type
                    )
            ):
                return {
                    "category": current_category,
                    "type": current_type,
                    "gender": current.get("gender"),
                    "occasion": current.get("occasion"),
                    "budget": current.get("budget")
                }

    merged = previous.copy()


    # -----------------------------------------
    # New shopping request?
    # Start a fresh conversation.
    # -----------------------------------------

    if (
        current.get("category")
        and
        current.get("category") != previous.get("category")
    ):
        return current

    # -----------------------------------------
    # Merge missing values
    # -----------------------------------------

    for key, value in current.items():

        if value not in [
            None,
            "",
            []
        ]:

            if key == "budget":

                try:
                    value = int(value)
                except:
                    pass

            merged[key] = value

    # -----------------------------------------
    # Keep previous values when user
    # only gives a follow-up like:
    #
    # under 3000
    # for office
    # for women
    # premium
    # black
    # etc.
    # -----------------------------------------

    for key in [
        "category",
        "type",
        "gender",
        "occasion",
        "budget"
    ]:

        if merged.get(key) is None:

            merged[key] = previous.get(key)

    return merged