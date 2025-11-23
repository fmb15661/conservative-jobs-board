import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_commonwealth():
    org = "Commonwealth Foundation"
    url = "https://commonwealthfoundation.org/careers/"

    print("Scraping Commonwealth Foundation…")

    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    # Find the "Open Positions" heading
    heading = soup.find("h2", id="h-open-positions")
    if not heading:
        # Fallback: search by text if id ever changes
        for h in soup.find_all(["h2", "h3"]):
            if "open positions" in h.get_text(strip=True).lower():
                heading = h
                break

    if not heading:
        print("Could not find 'Open Positions' section.")
    else:
        # Walk siblings after the heading until we hit another heading or end
        for sib in heading.find_all_next():
            # Stop when we hit another major heading
            if sib.name in ("h1", "h2", "h3") and sib is not heading:
                break

            # Each job is inside a <p><a>…</a></p>
            if sib.name == "p":
                a = sib.find("a", href=True)
                if not a:
                    continue

                title = a.get_text(strip=True)
                link = a["href"].strip()

                # Make absolute URL if needed
                if link.startswith("/"):
                    link = "https://commonwealthfoundation.org" + link

                jobs.append({
                    "title": title,
                    "organization": org,
                    "location": "",  # leave blank so you can fill manually
                    "url": link
                })

    # Save to frontend/public/jobs_commonwealth.json
    output_path = os.path.join(
        os.path.dirname(__file__),
        "../frontend/public/jobs_commonwealth.json"
    )
    output_path = os.path.abspath(output_path)

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Commonwealth job(s) to {output_path}")


if __name__ == "__main__":
    scrape_commonwealth()

