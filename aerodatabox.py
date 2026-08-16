import requests

url = "https://adsbexchange-com1.p.rapidapi.com/v2/lat/48.6899/lon/9.2219/dist/25/"

headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "adsbexchange-com1.p.rapidapi.com",
    "Accept-Encoding": "gzip"
}

response = requests.get(url, headers=headers, timeout=20)
response.raise_for_status()

data = response.json()
print(data)