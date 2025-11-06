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
        text = driver.find_element(By.TAG_NAME, "body").text

        if "The page can’t be found" in text:
            continue

        # Collapse whitespace
        text = re.sub(r"\s+", " ", text)

        # Find all "City, ST" pairs and take the LAST one
        matches = re.findall(r"[A-Z][a-zA-Z\s]+,\s?[A-Z]{2}", text)
        if matches:
            clean_loc = matches[-1].strip()
            # Keep only the last two words to avoid "Commerce Park Drive ..."
            parts = clean_loc.split()
            if len(parts) > 2:
                clean_loc = " ".join(parts[-2:])
            job["location"] = clean_loc

        # Detect job type if present
        if "Full-Time" in text or "Full Time" in text:
            job["type"] = "Full-Time"
        elif "Part-Time" in text or "Part Time" in text:
            job["type"] = "Part-Time"

    except Exception as e:
        print(f"⚠️ {job['link']} -> {e}")

driver.quit()

out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} YAF jobs to {out}")

