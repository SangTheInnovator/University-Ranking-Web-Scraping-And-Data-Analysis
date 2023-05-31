import json
import requests
from bs4 import BeautifulSoup as Soup

# Make a GET request to the URL
url = "https://en.wikipedia.org/wiki/List_of_IP_protocol_numbers"
response = requests.get(url)

table = Soup(response.content, "html.parser").find(
    "table", {"class": "wikitable"})

protocols = []

for entry in table.find_all("tr")[1:]:
    entries = entry.find_all("td")
    protocol_hex = entries[0].get_text(strip=True)
    protocol_number = entries[1].get_text(strip=True)
    protocol_name = entries[2].get_text(strip=True)
    protocol_description = entries[3].find("a")

    protocols.append({
        "Hex": protocol_hex,
        "Protocol Number": protocol_number,
        "Protocol Name": protocol_name,
        "Protocol Description": protocol_description
    })

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(protocols, f, default=list, ensure_ascii=False, indent=4)

