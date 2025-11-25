import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_heritage():
    print("Scraping Heritage…")

    url = "https://www.heritage.org/careers"
    org = "The Heritage Foundation"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("ERROR:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # This is the container you posted
    container = soup.select_one("div.about-careers__openings-links")
    if not container:
        print("ERROR: Could not find openings container.")
        return

    jobs = []

    for a in container.find_all("a"):
        title = a.get_text(strip=True)
        href = a["href"]

        # Default location
        location = "Washington, D.C."

        # Special case
        if "Northern-California" in href or "Pacific-Northwest" in href:
            location = "Remote (Northern California / Pacific Northwest)"

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": href
        })

    # Write the file to frontend/public
    output_path = os.path.abspath("../frontend/public/jobs_heritage.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Heritage job(s) to {output_path}")


if __name__ == "__main__":
    scrape_heritage()

