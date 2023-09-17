import requests
import json

# Define the URL of your Flask chatbot endpoint
url = 'http://192.168.56.1:5000/api/chatbot'

# Define the input text in a dictionary
payload = {'input_text': 'what is the universities mission statement.'}

# Send a POST request with JSON payload
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    chatbot_response = data.get('response')
    print("Chatbot Response:", chatbot_response)
else:
    print("Error:", response.status_code)