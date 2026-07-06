import google.generativeai as genai

genai.configure(
    api_key="AQ.Ab8RN6IPddTFUzR4yaaYVisKgYZjZvxeUKVQqG0FbMR2lNjRqQ"
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

response = model.generate_content(
    "Say hello"
)

print(response.text)