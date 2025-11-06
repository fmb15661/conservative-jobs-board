from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json, re, time

BASE_URL = "https://yaf.org/careers/"

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=opts)
driver.get(BASE_URL)
time.sleep(4)

jobs, seen = [], set()

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

for job in jobs:
    try:
        driver.get(job["link"])
        time.sleep(2)
        body_text = driver.find_element(By.TAG_NAME, "body").text

        if "The page can’t be found" in body_text:
            continue

        # Split by newlines and clean
        lines = [line.strip() for line in body_text.splitlines() if line.strip()]
        location_found = None

        # Find a line that looks like "City, ST"
        for line in lines:
            if re.match(r"^[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*,\s?[A-Z]{2}$", line):
                location_found = line
                break

        if location_found:
            job["location"] = location_found

        # Detect type if mentioned
        lower_text = body_text.lower()
        if "full-time" in lower_text or "full time" in lower_text:
            job["type"] = "Full-Time"
        elif "part-time" in lower_text or "part time" in lower_text:
            job["type"] = "Part-Time"

    except Exception as e:
        print(f"⚠️ {job['link']} -> {e}")

driver.quit()

out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} YAF jobs to {out}")

