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

# Gather job links
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

# Visit each page
for job in jobs:
    try:
        driver.get(job["link"])
        time.sleep(2)
        body = driver.find_element(By.TAG_NAME, "body").text
        lines = [line.strip() for line in body.splitlines() if line.strip()]

        # find job title and next line
        for i, line in enumerate(lines):
            if job["title"].lower() in line.lower():
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    # clean it up to just "City, ST"
                    match = re.search(r"[A-Z][a-zA-Z\s]+,\s?[A-Z]{2}", next_line)
                    if match:
                        job["location"] = match.group(0).strip()
                break

        # job type
        lower_body = body.lower()
        if "full-time" in lower_body or "full time" in lower_body:
            job["type"] = "Full-Time"
        elif "part-time" in lower_body or "part time" in lower_body:
            job["type"] = "Part-Time"

    except Exception as e:
        print(f"⚠️ {job['link']} -> {e}")

driver.quit()

out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} YAF jobs to {out}")

