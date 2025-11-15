import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def classify_type(title):
    t = title.lower()
    if any(k in t for k in ["policy", "analyst", "research", "fellow"]):
        return "Policy"
    if any(k in t for k in ["communications", "editor", "writer"]):
        return "Communications"
    if any(k in t for k in ["legal", "attorney", "counsel"]):
        return "Legal"
    if any(k in t for k in ["events", "operations", "manager", "coordinator"]):
        return "Operations"
    if "media" in t:
        return "Media"
    return "Other"


def scrape_claremont():
    url = "https://www.claremont.org/careers/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    jobs = []
    items = driver.find_elements(By.CSS_SELECTOR, ".careers-listing a")

    for item in items:
        try:
            title = item.text.strip()
            link = item.get_attribute("href")
        except:
            continue

        jobs.append({
            "title": title,
            "organization": "Claremont Institute",
            "location": "Claremont, CA",
            "type": classify_type(title),
            "link": link
        })

    driver.quit()

    with open("frontend/public/jobs_claremont.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ CLAREMONT: saved {len(jobs)} jobs → jobs_claremont.json")


if __name__ == "__main__":
    scrape_claremont()

