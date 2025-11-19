import requests
from bs4 import BeautifulSoup
import os
import json

URL = "https://alec.org/job-opportunities/"

def scrape_alec():
    try:
        html = requests.get(URL, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("Error fetching ALEC page:", e)
        return

    jobs = []

    # Each job is inside <li> with <h5 class="card-title"><a>
    for li in soup.select("ul.media-list li"):
        a = li.select_one("h5.card-title a")
        if not a:
            continue

        title = a.get_text(strip=True)
        link = a["href"].strip()

        jobs.append({
            "title": title,
            "company": "American Legislative Exchange Council (ALEC)",
            "location": "Washington, D.C.",
            "url": link,
            "type": "N/A"
        })

    # Save JSON in frontend/public/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "public", "jobs_alec.json")

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} ALEC jobs to {output_path}")

if __name__ == "__main__":
    scrape_alec()

