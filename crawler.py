import requests, os
from urllib.parse import urlparse

target_url = "https://tiobe.com/tiobe-index"

domaine = urlparse(target_url).netloc
domaine_name = domaine.split(".")[0]
page = urlparse(target_url).path

site_content = None

try:
    res = requests.get(target_url)
    res.raise_for_status()
    site_content = res.text
except requests.RequestException as e:
    print(f"Request failed: {e}")

if site_content:
    if not os.path.exists(f"sources/{domaine_name}"):
        os.makedirs(f"sources/{domaine_name}")
    with open(f"sources/{domaine_name}/{page}.html", "w", encoding="utf-8") as f:
        f.write(site_content)

print("Web content saved successfully")