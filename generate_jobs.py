import requests
from bs4 import BeautifulSoup
import json
import re

# Step 1: Scrape metadata from search results page
search_url = "https://careers.avasotech.com/search/?createNewAlert=false&q=&locationsearch="
search_html = requests.get(search_url).text
soup = BeautifulSoup(search_html, "html.parser")

# Extract job metadata
job_blocks = soup.find_all("tr")[1:]  # Skip header row
metadata = []
for block in job_blocks:
    cells = block.find_all("td")
    if len(cells) >= 5:
        metadata.append({
            "title": cells[0].text.strip(),
            "city": cells[1].text.strip(),
            "country": cells[2].text.strip(),
            "zip_code": cells[3].text.strip(),
            "post_date": cells[4].text.strip()
        })

# Step 2: Scrape job URLs from sitemap
sitemap_url = "https://careers.avasotech.com/sitemap.xml"
sitemap_xml = requests.get(sitemap_url).text
sitemap_soup = BeautifulSoup(sitemap_xml, "xml")
urls = sitemap_soup.find_all("loc")

# Extract job titles from URLs
job_links = []
for url in urls:
    link = url.text.strip()
    match = re.search(r'/job/(.*?)/\d+/', link)
    if match:
        title = match.group(1).replace("-", " ")
        job_links.append({
            "title": title.lower(),
            "url": link
        })

# Step 3: Merge metadata with URLs
enriched_jobs = []
for job in metadata:
    title_key = job["title"].lower()
    match = next((j for j in job_links if title_key in j["title"]), None)
    if match:
        job["url"] = match["url"]
        enriched_jobs.append(job)

# Step 4: Save to JSON
with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(enriched_jobs, f, indent=2, ensure_ascii=False)

print(f"✅ Scraped and saved {len(enriched_jobs)} enriched jobs.")


