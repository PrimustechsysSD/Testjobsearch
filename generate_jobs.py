import json
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Step 1: Scrape metadata from search page using Selenium
def scrape_search_metadata():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://careers.avasotech.com/search/?createNewAlert=false&q=&locationsearch=")
    time.sleep(5)  # Wait for JS to render

    rows = driver.find_elements("xpath", "//table[@id='searchresults']/tbody/tr")
    metadata = []
    for row in rows:
        cells = row.find_elements("tag name", "td")
        link = row.find_element("xpath", ".//a").get_attribute("href")
        match = re.search(r'/job/.+?/(\d+)/', link)
        if match and len(cells) >= 5:
            job_id = match.group(1)
            metadata.append({
                "job_id": job_id,
                "title": cells[0].text.strip(),
                "city": cells[1].text.strip(),
                "country": cells[2].text.strip(),
                "zip_code": cells[3].text.strip(),
                "post_date": cells[4].text.strip()
            })
    driver.quit()
    return metadata

# Step 2: Scrape job URLs from sitemap
def scrape_sitemap_urls():
    sitemap_url = "https://careers.avasotech.com/sitemap.xml"
    sitemap_xml = requests.get(sitemap_url).text
    soup = BeautifulSoup(sitemap_xml, "xml")
    urls = soup.find_all("loc")

    job_links = []
    for url in urls:
        link = url.text.strip()
        match = re.search(r'/job/.+?/(\d+)/', link)
        if match:
            job_id = match.group(1)
            job_links.append({
                "job_id": job_id,
                "url": link
            })
    return job_links

# Step 3: Merge metadata with URLs using job_id
def match_jobs(metadata, job_links):
    metadata_dict = {job["job_id"]: job for job in metadata}
    enriched_jobs = []
    for job in job_links:
        job_id = job["job_id"]
        if job_id in metadata_dict:
            enriched = {**metadata_dict[job_id], **job}
            enriched_jobs.append(enriched)
    return enriched_jobs

# Step 4: Save to JSON only if jobs found
def save_jobs(jobs):
    if jobs:
        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved {len(jobs)} enriched jobs.")
    else:
        print("⚠️ No jobs found. Skipping file write to preserve existing data.")

# Run the pipeline
if __name__ == "__main__":
    metadata = scrape_search_metadata()
    job_links = scrape_sitemap_urls()
    enriched_jobs = match_jobs(metadata, job_links)
    save_jobs(enriched_jobs)
