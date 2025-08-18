from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time

def scrape_search_metadata():
    # Configure headless Chrome options
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up ChromeDriver using Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Load the job search page
        url = "https://careers.avasotech.com/search/?createNewAlert=false&q=&locationsearch="
        driver.get(url)
        time.sleep(3)  # Allow time for dynamic content to load

        # Locate job cards
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-result")

        jobs = []
        for card in job_cards:
            try:
                title = card.find_element(By.CSS_SELECTOR, ".job-title").text
                location = card.find_element(By.CSS_SELECTOR, ".job-location").text
                link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

                jobs.append({
                    "title": title,
                    "location": location,
                    "link": link
                })
            except Exception as e:
                print(f"Error parsing job card: {e}")

        return jobs

    finally:
        driver.quit()

def save_to_json(data, filename="jobs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    metadata = scrape_search_metadata()
    save_to_json(metadata)
    print(f"✅ Saved {len(metadata)} jobs to jobs.json")
