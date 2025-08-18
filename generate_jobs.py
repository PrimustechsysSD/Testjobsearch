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
    try:
        # Extract job title from URL
        job_id = url.split("/job/")[1].split("/")[0]
        job_id = job_id.replace("-", " ")  # Optional: make it human-readable
    except IndexError:
        job_id = "unknown"
    jobs.append({
        "id": job_id,
        "url": url
    })

# Save to jobs.json
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Found {len(jobs)} jobs. jobs.json updated successfully.")
