from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import json
import time

def get_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_search_metadata():
    driver = get_chrome_driver()
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
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 5:
                        continue

                    title_elem = cells[0].find_element(By.CSS_SELECTOR, "a.jobTitle-link")
                    title = title_elem.text.strip()
                    link = title_elem.get_attribute("href")

                    city = cells[1].text.strip()
                    country = cells[2].text.strip()
                    zip_code = cells[3].text.strip()
                    post_date = cells[4].text.strip()

                    jobs.append({
                        "title": title,
                        "city": city,
                        "country": country,
                        "zip_code": zip_code,
                        "post_date": post_date,
                        "link": link
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
    print(f"✅ Saved {len(metadata)} jobs to jobs.json")
