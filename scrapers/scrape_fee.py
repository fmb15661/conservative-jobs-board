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

    # Find paragraphs that contain job links
    for p in soup.select("p"):
        # Find ALL bolded titles inside this <p>
        links = p.find_all("a")
        strongs = p.find_all("strong")

        if not links or not strongs:
            continue

        # Extract full text of paragraph to parse locations
        full_text = p.get_text(" ", strip=True)

        # Iterate through each job in this <p>
        for i in range(len(strongs)):
            title = strongs[i].get_text(strip=True)
            href = links[i]["href"]

            # Find the substring AFTER the title
            idx = full_text.find(title)
            remaining = full_text[idx + len(title):]

            # Extract location text up to next title (if any)
            if i + 1 < len(strongs):
                next_title = strongs[i+1].get_text(strip=True)
                next_idx = remaining.find(next_title)
                location_text = remaining[:next_idx]
            else:
                location_text = remaining

            location_text = location_text.replace("–", "").strip()

            # Normalize known location formats
            if "Virtual" in location_text:
                location = "Remote"
            elif "Atlanta" in location_text:
                location = "Hybrid/Atlanta, GA"
            else:
                location = location_text

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

