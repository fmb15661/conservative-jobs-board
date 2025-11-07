from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json, time

BASE_URL = "https://yaf.org/careers/"

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
driver.get(BASE_URL)
time.sleep(4)

jobs, seen = [], set()

# Collect job links
for a in driver.find_elements(By.CSS_SELECTOR, "a[href*='/careers/']"):
    href = a.get_attribute("href")
    if not href or "careers" not in href or href in seen:
        continue
    seen.add(href)
    title = a.text.strip()
    if not title or "Apply" in title or "Job" in title:
        continue
    jobs.append({
        "title": title,
        "organization": "Young America's Foundation",
        "location": "N/A",
        "type": "N/A",
        "link": href
    })

# Visit each job page
for job in jobs:
    try:
        driver.get(job["link"])
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, "body").text
        lines = [line.strip() for line in body.splitlines() if line.strip()]

        # Find the title line and take the next one as location
        for i, line in enumerate(lines):
            if job["title"].lower() in line.lower():
                if i + 1 < len(lines):
                    loc_line = lines[i + 1]
                    if "," in loc_line and len(loc_line.split(",")) == 2:
                        job["location"] = loc_line.strip()
                break

        # Detect job type if present
        text_lower = body.lower()
        if "full-time" in text_lower or "full time" in text_lower:
            job["type"] = "Full-Time"
        elif "part-time" in text_lower or "part time" in text_lower:
            job["type"] = "Part-Time"

    except Exception as e:
        print(f"⚠️ {job['link']} -> {e}")

driver.quit()

out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} YAF jobs to {out}")

