import requests
from bs4 import BeautifulSoup
import json

ACTON_URL = "https://www.acton.org/careers"
OUTPUT_FILE = "public/jobs_acton.json"

def scrape_acton():
    print("Requesting Acton careers page...")

    response = requests.get(ACTON_URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    job_items = soup.select("li.opening")

    print(f"Found {len(job_items)} Acton job cards")

    jobs = []

    for item in job_items:
        title_el = item.select_one(".opening__title a")
        loc_el = item.select_one(".opening__location")

        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        location = loc_el.get_text(strip=True) if loc_el else "N/A"
        link = "https://www.acton.org" + title_el.get("href")

        # Clean "Acton Institute | " prefix
        if "Acton Institute | " in location:
            location = location.replace("Acton Institute | ", "")

        jobs.append({
            "title": title,
            "organization": "Acton Institute",
            "location": location,
            "type": "N/A",
            "link": link
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Acton jobs to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_acton()

