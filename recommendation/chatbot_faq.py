def get_faq_response(message):

    message = message.lower().strip()

    # -----------------------------
    # SHIPPING
    # -----------------------------

    if any(word in message for word in [
        "shipping",
        "delivery"
    ]):

        return (
            "🚚 We deliver across India.\n\n"
            "Standard delivery usually takes 3–7 business days."
        )

    # -----------------------------
    # RETURNS
    # -----------------------------

    if any(word in message for word in [
        "return",
        "returns",
        "replace",
        "replacement",
        "exchange"
    ]):

        return (
            "🔄 Most products can be returned or exchanged within 7 days "
            "of delivery if they meet the return policy."
        )

    # -----------------------------
    # REFUND
    # -----------------------------

    if any(word in message for word in [
        "refund",
        "refunds"
    ]):

        return (
            "💰 Refunds are processed after the returned product passes "
            "quality inspection."
        )

    # -----------------------------
    # PAYMENT
    # -----------------------------

    if any(word in message for word in [
        "payment",
        "payments",
        "upi",
        "credit card",
        "debit card",
        "cod",
        "cash on delivery"
    ]):

        return (
            "💳 We support UPI, Debit Cards, Credit Cards, "
            "Net Banking and Cash on Delivery (COD) "
            "for eligible products."
        )

    # -----------------------------
    # CONTACT
    # -----------------------------

    if any(word in message for word in [
        "contact",
        "customer care",
        "support"
    ]):

        return (
            "📞 You can contact ShopSmart Customer Support "
            "through the Contact Us page."
        )

    return None