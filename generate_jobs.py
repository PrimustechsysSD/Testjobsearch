from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time

def scrape_search_metadata():
    # Configure headless Chrome options for CI environments
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Set up ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        jobs = []
        startrow = 0
        while True:
            # Paginated URL: 25 jobs per page
            url = f"https://careers.avasotech.com/search/?createNewAlert=false&q=&locationsearch=&startrow={startrow}"
            driver.get(url)
            time.sleep(3)  # Allow dynamic content to load

            job_rows = driver.find_elements(By.CSS_SELECTOR, "tr.data-row")
            if not job_rows:
                break  # No more jobs found

            for row in job_rows:
                try:
                    title_elem = row.find_element(By.CSS_SELECTOR, "a.jobTitle-link")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")

                    cells = row.find_elements(By.TAG_NAME, "td")
                    location = cells[1].text.strip() if len(cells) > 1 else "Unknown"

                    jobs.append({
                        "title": title,
                        "location": location,
                        "link": link
                    })
                except Exception as e:
                    print(f"⚠️ Skipped row due to error: {e}")

            startrow += 25  # Move to next page

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
