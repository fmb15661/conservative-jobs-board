from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json, time, re

BASE_URL = "https://yaf.org/careers/"

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
driver.get(BASE_URL)
time.sleep(4)

jobs, seen = [], set()

# collect links
for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='/careers/']"):
    href = a.get_attribute("href")
    if href and href.startswith(BASE_URL) and href not in seen and not href.endswith("careers/"):
        seen.add(href)
        title = a.text.strip()
        if title and len(title) > 2:
            jobs.append({
                "title": title,
                "organization": "Young America's Foundation",
                "location": "N/A",
                "type": "N/A",
                "link": href
            })

print(f"🧾 Found {len(jobs)} YAF job links")

# process each job page
for job in jobs:
    try:
        driver.get(job["link"])
        time.sleep(2)
        text = driver.find_element(By.TAG_NAME, "body").text
        lines = [l.strip() for l in text.splitlines() if l.strip()]

        # --- LOCATION ---
        for l in lines:
            if re.search(r"[A-Z][a-zA-Z\s]+,\s?(?:[A-Z]{2}|[A-Z][a-z]+)$", l):
                job["location"] = l.strip()
                break

        # --- TYPE (job category) ---
        lower = text.lower()

        if any(k in lower for k in ["policy", "research", "legislative", "analysis"]):
            job["type"] = "Policy"
        elif any(k in lower for k in ["development", "fundraising", "donor", "philanthropy"]):
            job["type"] = "Development"
        elif any(k in lower for k in ["communication", "media", "press", "public relations", "marketing", "journalism"]):
            job["type"] = "Communications"
        elif any(k in lower for k in ["education", "student", "teacher", "school", "campus"]):
            job["type"] = "Education"
        elif any(k in lower for k in ["event", "conference", "program", "outreach"]):
            job["type"] = "Programs"
        elif any(k in lower for k in ["finance", "accounting", "operations", "administration"]):
            job["type"] = "Operations"
        elif any(k in lower for k in ["graphic", "design", "creative", "digital", "video"]):
            job["type"] = "Creative / Digital"
        else:
            job["type"] = "N/A"

        print(f"✅ {job['title']} | {job['location']} | {job['type']}")

    except Exception as e:
        print(f"⚠️ Error on {job['link']}: {e}")

driver.quit()

# save
out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"\n✅ Saved {len(jobs)} YAF jobs to {out}")

