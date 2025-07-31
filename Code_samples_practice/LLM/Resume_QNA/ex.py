import requests

url = "https://api.chatanywhere.tech/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer sk-RXrtk8hjKveWu50JqpXAtEd7x0RgJADlqf0uDjWBNeCIVSOq"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "user",
            "content": "what is 2 + 2"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

print(result['choices'][0]['message']['content'])
