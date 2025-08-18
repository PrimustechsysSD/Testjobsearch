import requests
from bs4 import BeautifulSoup
import json

# Fetch sitemap
sitemap_url = "https://careers.avasotech.com/sitemap.xml"
response = requests.get(sitemap_url)
soup = BeautifulSoup(response.content, "lxml-xml")

# Extract job URLs
urls = [loc.text for loc in soup.find_all("loc") if "/job/" in loc.text]

jobs = []
for url in urls:
    try:
        job_id = url.split("/job/")[1].split("/")[0].replace("-", " ")
    except IndexError:
        job_id = "unknown"

    # Fetch job page
    job_response = requests.get(url)
    job_soup = BeautifulSoup(job_response.content, "html.parser")

    # Extract metadata
    title = job_soup.find("h1").text.strip() if job_soup.find("h1") else job_id
    location = job_soup.find("span", class_="job-location")
    city = job_soup.find("span", class_="job-city")
    department = job_soup.find("span", class_="job-department")
    posting_date = job_soup.find("span", class_="job-posting-date")

    jobs.append({
        "id": job_id,
        "title": title,
        "url": url,
        "location": location.text.strip() if location else "",
        "city": city.text.strip() if city else "",
        "department": department.text.strip() if department else "",
        "posting_date": posting_date.text.strip() if posting_date else ""
    })

# Save to jobs.json
with open("jobs.json", "w") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Enriched {len(jobs)} jobs with metadata.")

