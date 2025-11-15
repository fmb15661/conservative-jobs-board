import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def classify_type(title):
    t = title.lower()
    if any(k in t for k in ["policy", "analyst", "research", "economist"]):
        return "Policy"
    if any(k in t for k in ["communications", "social media", "editor", "writer", "podcast"]):
        return "Communications"
    if any(k in t for k in ["legal", "attorney", "counsel", "litigation"]):
        return "Legal"
    if any(k in t for k in ["government affairs", "lobby", "relations"]):
        return "Government Affairs"
    if any(k in t for k in ["media", "press"]):
        return "Media"
    if any(k in t for k in ["development", "operations", "manager", "coordinator", "assistant"]):
        return "Operations"
    return "Other"


def scrape_afpi():
    url = "https://americafirstpolicy.com/careers"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    jobs = []
    cards = driver.find_elements(By.CSS_SELECTOR, ".job-card")

    for c in cards:
        try:
            title = c.find_element(By.TAG_NAME, "h3").text.strip()
            link = c.find_element(By.TAG_NAME, "a").get_attribute("href")
            location = "Washington, DC"  # AFPI nearly always DC, page does not list per job
        except:
            continue

        jobs.append({
            "title": title,
            "organization": "America First Policy Institute",
            "location": location,
            "type": classify_type(title),
            "link": link
        })

    driver.quit()

    with open("frontend/public/jobs_afpi.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ AFPI: saved {len(jobs)} jobs → jobs_afpi.json")


if __name__ == "__main__":
    scrape_afpi()

