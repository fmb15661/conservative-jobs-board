import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_acton():
    url = "https://www.acton.org/careers"
    print("Requesting Acton careers page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    cards = soup.select("ul.careers-listing__internships li.opening")

    print(f"Found {len(cards)} Acton job cards")

    for card in cards:
        title_el = card.select_one(".opening__title a")
        loc_el = card.select_one(".opening__location")

        if not title_el:
            continue

        raw_title = title_el.get_text(strip=True)

        # ⭐ FIX: convert ALL CAPS to Title Case
        title = raw_title.title()

        location = loc_el.get_text(strip=True) if loc_el else "N/A"
        link = "https://www.acton.org" + title_el["href"]

        jobs.append({
            "title": title,
            "organization": "Acton Institute",
            "location": location,
            "type": "N/A",
            "link": link
        })

    # save
    output_path = os.path.join("public", "jobs_acton.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Acton jobs to {output_path}")


if __name__ == "__main__":
    scrape_acton()

