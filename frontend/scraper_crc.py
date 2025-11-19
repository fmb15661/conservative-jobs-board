import requests
from bs4 import BeautifulSoup
import os

def scrape_crc_internships():
    URL = "https://capitalresearch.org/about/internships/"

    try:
        html = requests.get(URL, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        print("Error fetching CRC page:", e)
        return

    internships = []

    # Find all <h4> headings with "Internship in"
    for h4 in soup.find_all("h4"):
        title_text = h4.get_text(strip=True)
        if title_text.lower().startswith("internship in"):
            internships.append({
                "title": title_text,
                "organization": "Capital Research Center",
                "location": "Washington, D.C.",
                "url": URL,
                "type": "N/A"
            })

    # Auto-locate the correct output path relative to THIS file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "public", "jobs_crc.json")

    # Save
    with open(output_path, "w") as f:
        import json
        json.dump(internships, f, indent=2)

    print(f"Saved {len(internships)} CRC internships to {output_path}")

if __name__ == "__main__":
    scrape_crc_internships()

