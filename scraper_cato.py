from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
import time

def scrape_cato_jobs():
    url = "https://recruiting.paylocity.com/recruiting/jobs/All/eb1d479c-5f1a-41bf-8916-c72467c0b7ca/Cato-Institute"
    print("Launching FULL Chrome (non-headless) for Cato...")

    options = Options()
    # REMOVE headless mode entirely
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    print("Waiting for job cards... (look at the Chrome window!)")

    try:
        job_cards = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "job-listing"))
        )
    except Exception as e:
        print("❌ Job cards did not appear")
        print(str(e))
        driver.quit()
        return []

    jobs = []

    for card in job_cards:
        try:
            title = card.find_element(By.TAG_NAME, "h3").text.strip()
        except:
            title = "N/A"

        try:
            location = card.find_element(By.CLASS_NAME, "job-location").text.strip()
        except:
            location = "N/A"

        try:
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
        except:
            link = "N/A"

        jobs.append({
            "title": title,
            "organization": "Cato Institute",
            "location": location,
            "type": "N/A",
            "date_posted": "N/A",
            "link": link
        })

    driver.quit()
    return jobs

if __name__ == "__main__":
    jobs = scrape_cato_jobs()
    output_path = os.path.join("public", "jobs_cato.json")

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"\nScraped {len(jobs)} Cato jobs and saved to {output_path}")

