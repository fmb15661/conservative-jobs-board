import requests
from bs4 import BeautifulSoup
import json

def scrape_heritage_jobs():
    url = "https://www.heritage.org/careers"
    print("Requesting Heritage careers page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Heritage job cards
    job_cards = soup.select(".views-row")
    print(f"Found {len(job_cards)} Heritage job cards")

    for card in job_cards:
        title_el = card.select_one("h3")
        location_el = card.select_one(".field--name-field-location")
        link_el = card.select_one("a")

        title = title_el.get_text(strip=True) if title_el else "N/A"
        location = location_el.get_text(strip=True) if location_el else "N/A"
        link = "https://www.heritage.org" + link_el.get("href") if link_el else "N/A"

        jobs.append({
            "title": title,
            "organization": "Heritage Foundation",
            "location": location,
            "type": "N/A",
            "link": link
        })

    # Save JSON
    output_path = "public/jobs_heritage.json"
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Heritage jobs to {output_path}")


if __name__ == "__main__":
    scrape_heritage_jobs()

