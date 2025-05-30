import requests

url = "https://api.example.com/data"
headers = {
    "Authorization":"Bearer your_token"
}
params = {
    "param": "value"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
print(data)