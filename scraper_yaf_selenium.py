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
        lines = [line.strip() for line in driver.find_element(By.TAG_NAME, "body").text.splitlines() if line.strip()]
        text = " ".join(lines).lower()

        # --- detect location (look 1 or 2 lines below title) ---
        for i, line in enumerate(lines):
            if job["title"].lower() in line.lower():
                for offset in [1, 2]:
                    if i + offset < len(lines):
                        test_line = lines[i + offset]
                        match = re.search(r"[A-Z][a-zA-Z\s]+,\s?(?:[A-Z]{2}|[A-Z][a-z]+)$", test_line)
                        if match:
                            job["location"] = match.group(0).strip()
                            break
                break

        # --- detect type (more robust) ---
        if re.search(r"\bfull[-\s]?time\b", text):
            job["type"] = "Full-Time"
        elif re.search(r"\bpart[-\s]?time\b", text):
            job["type"] = "Part-Time"
        elif re.search(r"\bintern(ship)?\b", text):
            job["type"] = "Internship"
        elif re.search(r"\bcontract\b", text):
            job["type"] = "Contract"
        elif re.search(r"\btemporary\b", text):
            job["type"] = "Temporary"

    except Exception as e:
        print(f"⚠️ {job['link']} -> {e}")

driver.quit()

out = "frontend/public/jobs_yaf.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} YAF jobs to {out}")

