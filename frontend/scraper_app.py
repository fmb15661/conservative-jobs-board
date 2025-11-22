import requests
from bs4 import BeautifulSoup
import json

URL = "https://americanprinciplesproject.org/careers/"
OUTPUT = "public/jobs_app.json"

def scrape_app():
    print("Fetching APP job postings...")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    # APP uses <h2> for each job title
    titles = soup.find_all("h2")

    for h2 in titles:
        title = h2.get_text(strip=True)

        # Each job block is followed by <p><strong>Reports to:</strong>...
        block = []
        sibling = h2.find_next_sibling()

        while sibling and sibling.name == "p":
            block.append(sibling.get_text(" ", strip=True))
            sibling = sibling.find_next_sibling()

        description_text = " ".join(block)

        # Extract location (appears as "Location: Arlington, VA")
        location = "N/A"
        for line in block:
            if "Location:" in line:
                location = line.replace("Location:", "").strip()

        job = {
            "title": title,
            "organization": "American Principles Project",
            "location": location,
            "url": URL,  # All jobs on one page
            "type": "N/A"
        }

        jobs.append(job)

    print(f"Found {len(jobs)} APP job(s). Saving...")

    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved APP jobs to {OUTPUT}")

if __name__ == "__main__":
    scrape_app()

