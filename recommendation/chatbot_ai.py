import json
import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def extract_ai_intent(query):
    prompt = f"""
    You are ShopSmart's AI Shopping Intent Extractor.

    Your task is to convert a customer's shopping request into JSON.

    Return ONLY valid JSON.

    Schema:

    {{
        "category": null,
        "type": null,
        "gender": null,
        "occasion": null,
        "budget": null
    }}

    Allowed categories:

    clothing
    footwear
    bags
    watches
    beauty
    furniture
    sports
    jewellery
    pet supplies

    Recognize natural shopping language.

    Examples

    User:
    I need something to carry my laptop.

    Output:
    {{
        "category":"bags",
        "type":"laptop",
        "gender":null,
        "occasion":"office",
        "budget":null
    }}

    User:
    I'm joining college next month.

    Output:
    {{
        "category":"bags",
        "type":"backpack",
        "gender":null,
        "occasion":"college",
        "budget":null
    }}

    User:
    I need comfortable shoes for walking.

    Output:
    {{
        "category":"footwear",
        "type":"shoes",
        "gender":null,
        "occasion":"walking",
        "budget":null
    }}

    User:
    I have an interview tomorrow.

    Output:
    {{
        "category":"clothing",
        "type":"shirt",
        "gender":null,
        "occasion":"interview",
        "budget":null
    }}

    User:
    I'm going to Goa.

    Output:
    {{
        "category":"clothing",
        "type":"casual",
        "gender":null,
        "occasion":"travel",
        "budget":null
    }}

    User:
    Need something for trekking.

    Output:
    {{
        "category":"footwear",
        "type":"sports shoes",
        "gender":null,
        "occasion":"trekking",
        "budget":null
    }}

    User:
    Need something for gym workouts.

    Output:
    {{
        "category":"sports",
        "type":"fitness",
        "gender":null,
        "occasion":"gym",
        "budget":null
    }}

    User:
    Gift for my wife under 3000.

    Output:
    {{
        "category":"bags",
        "type":"handbag",
        "gender":"women",
        "occasion":"gift",
        "budget":3000
    }}

    User:
    Gift for my father.

    Output:
    {{
        "category":"watches",
        "type":"watch",
        "gender":"men",
        "occasion":"gift",
        "budget":null
    }}

    User:
    Need something for rainy season.

    Output:
    {{
        "category":"footwear",
        "type":"sandals",
        "gender":null,
        "occasion":"rain",
        "budget":null
    }}

    User:
    Suggest something for office meetings.

    Output:
    {{
        "category":"clothing",
        "type":"shirt",
        "gender":null,
        "occasion":"office",
        "budget":null
    }}

    User:
    Recommend premium backpacks under 4000.

    Output:
    {{
        "category":"bags",
        "type":"backpack",
        "gender":null,
        "occasion":null,
        "budget":4000
    }}

    User Query:

    {query}
    """

    try:

        response = model.generate_content(prompt)

        text = (
            response.text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        intent = json.loads(text)

        if (
                "goes with" in query
                or "matches with" in query
                or "match with" in query
                or "what matches" in query
                or "wear with" in query
        ):
            intent["occasion"] = "style_match"

        # Normalize Gemini outputs

        if intent.get("occasion") == "campus":
            intent["occasion"] = "college"

        if (
                intent.get("occasion") == "college"
                and not intent.get("category")
        ):
            intent["category"] = "footwear"
            intent["type"] = "shoes"

        if (
                intent.get("occasion") == "daily"
                and not intent.get("category")
        ):
            intent["category"] = "footwear"
            intent["type"] = "shoes"

        if (
                intent.get("occasion") == "office"
                and intent.get("category") == "footwear"
        ):
            intent["category"] = "clothing"
            intent["type"] = "shirt"

        return intent

    except Exception as e:

        print("AI INTENT ERROR =", e)

        from recommendation.chatbot_intent import (
            extract_chatbot_intent
        )

        return extract_chatbot_intent(query)