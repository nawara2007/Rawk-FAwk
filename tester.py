import requests
import os

# import json
import json
symbol="nflx"
response = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={os.environ.get("API_KEY")}')
data = json.loads(response.text)

# Access the desired value
# try:
price = data['AnalystTargetPrice']
CompanyName = data['Name']
ans = {
    "name": CompanyName,
    "price": float(price),
    "symbol": symbol
}
# except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
    # return None
print(ans)