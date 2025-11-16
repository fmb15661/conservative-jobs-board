import requests
from bs4 import BeautifulSoup
import json
import os

PLF_URL = "https://pacificlegal.org/careers/"

OUTPUT_FILE = "public/jobs_plf.json"


def clean_location(text):
    """Normalize PLF location lines."""
    if not text:
        return "N/A"

    # Fix the “Fully Remote • Work from Anywhere in the U.S.” issue
    if "Fully Remote" in text or "Work from Anywhere" in text:
        return "Virtual"

    return text.strip()


def scrape_plf_jobs():
    print("Requesting PLF careers page...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(PLF_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.select(".career-item")
    print(f"Found {len(job_cards)} PLF job cards\n")

    results = []

    for card in job_cards:
        # TITLE
        title_el = card.find("h2")
        title = title_el.get_text(strip=True) if title_el else "N/A"

        # LOCATION — ONLY pull from <em>, NEVER from paragraphs
        loc_el = card.find("em")
        location = clean_location(loc_el.get_text(strip=True) if loc_el else "N/A")

        # APPLY LINK
        apply_el = card.find("a", class_="button")
        link = apply_el["href"] if apply_el else "N/A"

        print(f"Scraped job: {title} — {location}")

        results.append({
            "title": title,
            "organization": "Pacific Legal Foundation",
            "location": location,
            "type": "N/A",
            "date_posted": "N/A",
            "link": link
        })

    # SAVE JSON
    full_path = os.path.join(os.getcwd(), OUTPUT_FILE)

    with open(full_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved {len(results)} PLF jobs to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape_plf_jobs()

