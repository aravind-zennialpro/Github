import requests

# Replace with your actual Gemini API key
api_key = "3313d628dbe3466e9f1567ac26c956d4"  # 🔑 Replace with your key

# Gemini Flash API endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

# Get user input dynamically
user_question = input("❓ Ask something to Gemini AI: ")

# Request payload
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": user_question
                }
            ]
        }
    ]
}

# Request headers
headers = {
    "Content-Type": "application/json"
}

try:
    # Send POST request
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise error for HTTP issues

    # Extract and print the AI's reply
    reply = response.json()['candidates'][0]['content']['parts'][0]['text']
    print("\n🤖 Gemini says:", reply)

except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)
except KeyError:
    print("❌ Unexpected response format:", response.text)
