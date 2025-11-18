import requests
from bs4 import BeautifulSoup
import json
import re

NTU_URL = "https://www.ntu.org/about/page/career-and-internship-opportunities"
OUTPUT_FILE = "public/jobs_ntu.json"

def clean_title(title):
    """
    Remove salary ranges like:
    - Salary Range [$100,000-150,000]
    - - [$25/hour]
    - anything inside brackets following a dash
    """
    # Remove anything after a dash that contains a bracket
    return re.sub(r"-\s*\[.*?\]", "", title).strip()

def scrape_ntu():
    print("Requesting NTU job listings...")

    response = requests.get(NTU_URL, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Look for all <a> tags that link to ApplyToJob.com
    job_links = soup.find_all("a", href=lambda x: x and "applytojob.com" in x)

    for link in job_links:
        raw_title = link.text.strip()
        title = clean_title(raw_title)

        jobs.append({
            "title": title,
            "organization": "National Taxpayers Union",
            "location": "Washington, DC (Hybrid/Remote)",  # NTU lists DC but allows remote work
            "type": "N/A",
            "link": link["href"]
        })

        print(f"Scraped job: {title}")

    # Save JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"\nSaved {len(jobs)} NTU jobs to {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_ntu()

