import requests
from bs4 import BeautifulSoup
import json

URL = "https://americanprinciplesproject.org/careers/"
OUTPUT = "frontend/public/jobs_app.json"

def scrape_app():
    print("Fetching APP job postings...")

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []
    job_sections = soup.find_all("h2")

    for h2 in job_sections:
        title = h2.get_text(strip=True)
        section = h2.find_next("p")
        location = ""
        link = URL

        if section:
            strongs = section.find_all("strong")
            for s in strongs:
                if "Location" in s.get_text():
                    location = s.next_sibling.strip() if s.next_sibling else ""

        jobs.append({
            "title": title,
            "organization": "American Principles Project",
            "location": location,
            "url": URL
        })

    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} APP jobs → {OUTPUT}")

if __name__ == "__main__":
    scrape_app()

