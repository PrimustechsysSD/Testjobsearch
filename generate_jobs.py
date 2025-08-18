import requests
from bs4 import BeautifulSoup
import json

# Fetch sitemap
sitemap_url = "https://careers.avasotech.com/sitemap.xml"
response = requests.get(sitemap_url)
soup = BeautifulSoup(response.content, "lxml-xml")  # Use lxml parser for XML

# Extract job URLs
urls = [loc.text for loc in soup.find_all("loc") if "/job/" in loc.text]

# Build job entries
jobs = []
for url in urls:
    job_id = url.split("/")[-1].split("?")[0]  # Extract job ID from URL
    jobs.append({
        "id": job_id,
        "url": url
    })

# Save to jobs.json
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Found {len(jobs)} jobs. jobs.json updated successfully.")
