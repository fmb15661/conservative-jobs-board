import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://yaf.org/careers/"
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []

# Find all job blocks (YAF uses <a> links inside job listings)
for a in soup.select("a[href*='/careers/']"):
    href = a["href"]
    if not href.startswith("http"):
        href = "https://yaf.org" + href

    title = a.get_text(strip=True)
    if not title or "Apply" in title or "Job" in title:
        continue

    job = {
        "title": title,
        "organization": "Young America's Foundation",
        "location": "N/A",
        "type": "N/A",
        "date_posted": "N/A",
        "link": href,
    }

    # Visit each job page to extract more details
    try:
        job_page = requests.get(href, timeout=10)
        job_soup = BeautifulSoup(job_page.text, "html.parser")

        # Look for text patterns that might contain location or date
        text = job_soup.get_text(" ", strip=True)

        # Common patterns YAF uses
        if "Reston" in text:
            job["location"] = "Reston, VA"
        elif "Santa Barbara" in text:
            job["location"] = "Santa Barbara, CA"
        elif "Nashville" in text:
            job["location"] = "Nashville, TN"
        elif "Irving" in text:
            job["location"] = "Irving, TX"
        elif "Washington" in text:
            job["location"] = "Washington, DC"

        # Date posted (look for month names)
        import re

        m = re.search(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}",
            text,
        )
        if m:
            job["date_posted"] = m.group(0)

        # Type (look for "Full-Time" or "Part-Time")
        if "Full-Time" in text or "Full Time" in text:
            job["type"] = "Full-Time"
        elif "Part-Time" in text or "Part Time" in text:
            job["type"] = "Part-Time"

    except Exception as e:
        print(f"Error scraping {href}: {e}")

    jobs.append(job)

# Save to JSON
output_path = "frontend/public/jobs_yaf.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=2)

print(f"✅ Saved {len(jobs)} jobs to {output_path}")

