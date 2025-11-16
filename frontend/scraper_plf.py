import requests
from bs4 import BeautifulSoup
import json
import os

PLF_URL = "https://pacificlegal.org/careers/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

OUTPUT_FILE = "public/jobs_plf.json"


def scrape_plf_jobs():
    print("Requesting PLF careers page...")

    response = requests.get(PLF_URL, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.select("div.career-item")

    print(f"Found {len(job_cards)} PLF job cards\n")

    jobs = []

    for card in job_cards:
        title_el = card.find("h2")
        title = title_el.text.strip() if title_el else "N/A"

        # Location handling
        loc_el = card.find("p")
        location = loc_el.text.strip() if loc_el else "N/A"

        # Convert ONLY the remote text into "Virtual"
        if "Fully Remote" in location and "Work from Anywhere" in location:
            location = "Virtual"

        # Apply link
        apply_el = card.find("a", class_="button")
        link = apply_el["href"] if apply_el and apply_el.has_attr("href") else "N/A"

        jobs.append({
            "title": title,
            "organization": "Pacific Legal Foundation",
            "location": location,
            "type": "N/A",
            "date_posted": "N/A",
            "link": link
        })

        print(f"Scraped job: {title} — {location}")

    # Save JSON
    out_path = os.path.join(os.getcwd(), OUTPUT_FILE)
    with open(out_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"\nSaved {len(jobs)} PLF jobs to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_plf_jobs()

