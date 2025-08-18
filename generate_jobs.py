from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time

def scrape_job_details(driver, url):
    driver.get(url)
    time.sleep(2)

    try:
        post_date = driver.find_element(By.CSS_SELECTOR, ".job-date").text.strip()
    except:
        post_date = "Unknown"

    try:
        location_details = driver.find_element(By.CSS_SELECTOR, ".job-location").text.strip()
    except:
        location_details = "Unknown"

    try:
        description = driver.find_element(By.CSS_SELECTOR, ".job-description").text.strip()
    except:
        description = "Not available"

    try:
        country = driver.find_element(By.CSS_SELECTOR, ".job-country").text.strip()
    except:
        country = "Unknown"

    try:
        zip_code = driver.find_element(By.CSS_SELECTOR, ".job-postalcode").text.strip()
    except:
        zip_code = "Unknown"

    return {
        "post_date": post_date,
        "location_details": location_details,
        "description": description,
        "country": country,
        "zip_code": zip_code
    }

def scrape_search_metadata():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        jobs = []
        startrow = 0
        while True:
            url = f"https://careers.avasotech.com/search/?createNewAlert=false&q=&locationsearch=&startrow={startrow}"
            driver.get(url)
            time.sleep(3)

            job_rows = driver.find_elements(By.CSS_SELECTOR, "tr.data-row")
            if not job_rows:
                break

            for row in job_rows:
                try:
                    title_elem = row.find_element(By.CSS_SELECTOR, "a.jobTitle-link")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")

                    cells = row.find_elements(By.TAG_NAME, "td")
                    location = cells[1].text.strip() if len(cells) > 1 else "Unknown"

                    # Enrich with detail page metadata
                    details = scrape_job_details(driver, link)

                    jobs.append({
                        "title": title,
                        "location": location,
                        "link": link,
                        "post_date": details["post_date"],
                        "location_details": details["location_details"],
                        "country": details["country"],
                        "zip_code": details["zip_code"],
                        "description": details["description"]
                    })
                except Exception as e:
                    print(f"⚠️ Skipped row due to error: {e}")

            startrow += 25

        return jobs

    finally:
        driver.quit()

def save_to_json(data, filename="jobs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    metadata = scrape_search_metadata()
    save_to_json(metadata)
    print(f"✅ Saved {len(metadata)} enriched jobs to jobs.json")
