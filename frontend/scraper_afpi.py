import requests
from bs4 import BeautifulSoup
import json

URL = "https://americafirstpolicy.com/careers"
OUTPUT_FILE = "frontend/public/jobs_afpi.json"

def scrape_afpi():
    response = requests.get(URL, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    listings = soup.find_all("a", class_="career")

    for job in listings:
        title_tag = job.find("h2")
        link = job.get("href")

        if not title_tag or not link:
            continue

        title = title_tag.get_text(strip=True)

        # Build full working URL
        if link.startswith("/"):
            link = "https://americafirstpolicy.com" + link

        job_entry = {
            "title": title,
            "company": "America First Policy Institute",
            "location": "Washington, D.C.",
            "type": "",
            "link": link
        }

        jobs.append(job_entry)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} AFPI jobs to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_afpi()

