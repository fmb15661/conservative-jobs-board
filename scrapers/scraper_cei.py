import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def classify_type(title):
    t = title.lower()
    if any(k in t for k in ["policy", "analyst", "research", "fellow"]):
        return "Policy"
    if any(k in t for k in ["communications", "writer", "editor"]):
        return "Communications"
    if any(k in t for k in ["legal", "attorney"]):
        return "Legal"
    if "media" in t:
        return "Media"
    if any(k in t for k in ["development", "manager", "coordinator"]):
        return "Operations"
    return "Other"


def scrape_cei():
    url = "https://cei.org/about/internships-jobs-and-fellowships/"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(3)

    jobs = []
    items = driver.find_elements(By.CSS_SELECTOR, "a")

    for i in items:
        text = i.text.strip()
        if not text:
            continue
        if "Apply" in text or "Intern" in text or "Director" in text or "Fellow" in text:
            try:
                link = i.get_attribute("href")
                title = text
                location = "Washington, DC"
            except:
                continue

            jobs.append({
                "title": title,
                "organization": "Competitive Enterprise Institute",
                "location": location,
                "type": classify_type(title),
                "link": link
            })

    driver.quit()

    with open("frontend/public/jobs_cei.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"✅ CEI: saved {len(jobs)} jobs → jobs_cei.json")


if __name__ == "__main__":
    scrape_cei()

