import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_bri():
    url = "https://billofrightsinstitute.org/about-bri/join-our-team"
    org = "Bill of Rights Institute"

    print(f"Scraping {org}...")

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Each job appears inside: <div class="mb-20 border rounded ...">
    job_cards = soup.select("div.mb-20.border.rounded")

    for card in job_cards:
        # Extract job title
        title_tag = card.find("h3")
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)

        # There is no direct job link — the "Apply Now" button
        # opens a modal, so we link to the main job page
        job_url = url  # fallback

        # Extract location
        location = "N/A"
        loc_p = card.find("p", string=lambda t: t and "Location:" in t)
        if loc_p:
            text = loc_p.get_text(strip=True)
            try:
                location = text.split("Location:")[1].strip()
            except:
                pass

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": job_url
        })

    # Write JSON to frontend/public
    output_path = os.path.join(
        os.path.dirname(__file__),
        "../frontend/public/jobs_bri.json"
    )
    output_path = os.path.abspath(output_path)

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} BRI job(s) to {output_path}")


if __name__ == "__main__":
    scrape_bri()

