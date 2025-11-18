import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_ntu():
    url = "https://www.ntu.org/about/page/career-and-internship-opportunities"
    print("Requesting NTU careers page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.select_one(".rich-text-content")
    if not container:
        print("❌ Could not find .rich-text-content section")
        return

    jobs = []

    # Get all <a> links inside the rich text
    links = container.find_all("a")
    print(f"Found {len(links)} total <a> tags inside content")

    for a in links:
        href = a.get("href", "")
        text = a.get_text(strip=True)

        # Only take job links that go to ApplyToJob
        if "applytojob.com/apply" not in href:
            continue

        title = text
        link = href
        location = "Washington, DC"  # You confirmed each job shows location

        jobs.append({
            "title": title,
            "organization": "National Taxpayers Union",
            "location": location,
            "type": "N/A",
            "link": link
        })

        print("Scraped job:", title)

    output_path = os.path.join("public", "jobs_ntu.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"\nSaved {len(jobs)} NTU jobs to public/jobs_ntu.json")


if __name__ == "__main__":
    scrape_ntu()

