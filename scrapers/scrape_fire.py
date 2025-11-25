import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_fire():
    print("Scraping Foundation for Individual Rights and Expression (FIRE)…")

    url = "https://www.thefire.org/careers"
    org = "Foundation for Individual Rights and Expression (FIRE)"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("ERROR:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    # Each job is inside <li class="accordion-item">
    for li in soup.select("li.accordion-item"):
        title_tag = li.select_one(".position-title")
        link_tag = li.select_one("a.arrow-link")

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag["href"]

        # Make absolute URL
        if link.startswith("/"):
            link = "https://www.thefire.org" + link

        # FIRE does not list location individually → set consistent location
        location = "Hybrid/Philadelphia, PA or Washington, D.C."

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": link
        })

    # Save JSON to frontend/public/
    output_path = os.path.abspath("../frontend/public/jobs_fire.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} FIRE job(s) to {output_path}")


if __name__ == "__main__":
    scrape_fire()

