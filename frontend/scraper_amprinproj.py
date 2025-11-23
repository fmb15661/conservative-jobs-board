import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://americanprinciplesproject.org/careers/"
OUTPUT = "frontend/public/jobs_amprinproj.json"

def scrape_amprinproj():
    print("Fetching American Principles Project jobs...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        )
    }

    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    # All job titles are under <h2>
    for h2 in soup.find_all("h2"):
        title = h2.get_text(strip=True)

        # Skip “Internships”, not a job
        if "Internship" in title or "Intern" in title:
            continue

        # Get location from next <p> tags
        location = "N/A"
        p = h2.find_next("p")
        while p:
            txt = p.get_text(strip=True)
            if "Location:" in txt:
                location = txt.split("Location:", 1)[1].strip()
                break
            # stop if we hit the next <h2>
            if p.name == "h2":
                break
            p = p.find_next("p")

        jobs.append({
            "title": title,
            "organization": "American Principles Project",
            "location": location,
            "type": "N/A",
            "link": URL
        })

    print(f"Found {len(jobs)} jobs")

    # Ensure folder exists
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    # Write JSON
    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved → {OUTPUT}")


if __name__ == "__main__":
    scrape_amprinproj()

