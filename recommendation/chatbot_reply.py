def format_products(products):

    reply = ""

    for _, product in products.iterrows():

        reply += f"""
        <div style='margin-bottom:15px;'>

            <img
                src="/static/{product['image']}"
                width="80"
                height="80"
                style="border-radius:5px;"
                onerror="this.src='/static/images/no_image.jpg';"
            >

            <br><br>

            ⭐ {product["product_name"]}

            <br>

            💰 ₹{product["price"]}

            <br>

            ⭐ Rating: {product["rating"]}

            <br><br>

            <a
                href="/recommend/{product['product_id']}"
                style="
                    background:#ff9900;
                    color:white;
                    padding:6px 12px;
                    border-radius:5px;
                    text-decoration:none;
                    display:inline-block;
                "
            >
                View Product
            </a>

        </div>
        """

    return reply