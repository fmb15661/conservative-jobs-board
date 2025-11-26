import requests
from bs4 import BeautifulSoup
import json

URL = "https://acc.eco/careers/"
OUTPUT = "public/jobs_acc.json"

def scrape_acc():
    resp = requests.get(URL, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")

    jobs = []

    cards = soup.select("article.job-card h3.card-title a.card-link")

    for a in cards:
        title = a.get_text(strip=True)
        url = a["href"]

        jobs.append({
            "title": title,
            "organization": "American Conservation Coalition",
            "location": "N/A",
            "url": url,
            "type": "N/A"
        })

    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} ACC jobs to {OUTPUT}")

if __name__ == "__main__":
    scrape_acc()

