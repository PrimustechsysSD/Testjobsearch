import requests
from bs4 import BeautifulSoup
import json

sitemap_url = "https://careers.avasotech.com/sitemap.xml"
response = requests.get(sitemap_url)
soup = BeautifulSoup(response.content, "xml")

jobs = []
for loc in soup.find_all("loc"):
    url = loc.text
    if "/job/" in url:
        title = url.split("/job/")[1].split("/")[0]
        title = title.replace("-", " ").replace("&", "&amp;").strip()
        jobs.append({"title": title, "url": url})

with open("jobs.json", "w") as f:
    json.dump({"jobs": jobs}, f, indent=2)
