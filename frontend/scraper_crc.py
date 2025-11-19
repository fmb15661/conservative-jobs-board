import requests
from bs4 import BeautifulSoup
import os
import json

def scrape_crc_internships():
    URL = "https://capitalresearch.org/about/internships/"

    try:
        html = requests.get(URL, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("Error fetching CRC page:", e)
        return

    internships = []

    # Detect all internship headings
    for h4 in soup.find_all("h4"):
        title_text = h4.get_text(strip=True)
        if title_text.lower().startswith("internship in"):
            internships.append({
                "title": title_text,
                "organization": "Capital Research Center",
                "location": "Washington, D.C.",
                "link": URL,           # FIXED KEY
                "type": "N/A"
            })

    # Safe path resolution
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "public", "jobs_crc.json")

    with open(output_path, "w") as f:
        json.dump(internships, f, indent=2)

    print(f"Saved {len(internships)} CRC internships to {output_path}")

if __name__ == "__main__":
    scrape_crc_internships()

