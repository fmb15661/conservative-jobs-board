import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_fee():
    print("Scraping Foundation for Economic Education (FEE)…")

    url = "https://fee.org/about/job-openings/"
    org = "Foundation for Economic Education (FEE)"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("ERROR:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    jobs = []

    # Look for <p><a><strong>Title</strong></a> – Location text inside <p>
    for p in soup.select("p"):
        link = p.find("a")
        strong = p.find("strong")

        if not link or not strong:
            continue

        title = strong.get_text(strip=True)
        href = link["href"]

        text = p.get_text(" ", strip=True)

        # Detect location
        location = ""
        if "Virtual" in text:
            location = "Remote"
        elif "Atlanta preferred" in text:
            location = "Hybrid/Atlanta, GA"

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": href
        })

    # Write JSON file to frontend/public
    output_path = os.path.abspath("../frontend/public/jobs_fee.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} FEE job(s) to {output_path}")


if __name__ == "__main__":
    scrape_fee()

