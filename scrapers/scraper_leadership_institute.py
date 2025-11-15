import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def classify_type(title):
    t = title.lower()
    if any(k in t for k in ["policy", "analyst", "research"]):
        return "Policy"
    if any(k in t for k in ["communications", "editor", "writer"]):
        return "Communications"
    if any(k in t for k in ["legal", "attorney", "counsel"]):
        return "Legal"
    if any(k in t for k in ["field", "organizer", "operations", "manager", "coordinator"]):
        return "Operations"
    if "media" in t:
        return "Media"
    return "Other"


def scrape_leadership_institute():
    url = "https://www.leadershipinstitute.org/jobs/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    jobs = []
    rows = driver.find_elements(By.CSS_SELECTOR, ".careers-listing a")

    for row in rows:
        try:
            title = row.text.strip()
            link = row.get_attribute("href")
        except:
            continue

        jobs.append({
            "title": title,
            "organization": "Leadership Institute",
            "location": "Arlington, VA",
            "type": classify_type(title),
            "link": link
        })

    driver.quit()

    with open("frontend/public/jobs_leadership_institute.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ LEADERSHIP INSTITUTE: saved {len(jobs)} jobs → jobs_leadership_institute.json")


if __name__ == "__main__":
    scrape_leadership_institute()

