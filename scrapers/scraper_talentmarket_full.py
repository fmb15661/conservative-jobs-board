import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

BASE = "https://talentmarket.org/job-openings/page/{}/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def scrape_page(page_num):
    url = BASE.format(page_num)
    print("Scraping:", url)
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        print("blocked:", r.status_code)
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    listings = soup.select("article.job-opening")

    jobs = []
    for article in listings:
        title_tag = article.select_one("h2.entry-title a")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag["href"]

        meta = article.select_one("p.job-meta")
        org = "Unknown"
        location = "Unknown"

        if meta:
            text = meta.get_text(strip=True)
            if "|" in text:
                parts = text.split("|")
                org = parts[0].strip()
                location = parts[1].strip()

        date_tag = article.select_one("time")
        posted = "1970-01-01"
        if date_tag:
            posted = datetime.strptime(date_tag.get_text(strip=True), "%B %d, %Y").strftime("%Y-%m-%d")

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "type": "N/A",
            "date_posted": posted,
            "link": link
        })

    return jobs

def main():
    all_jobs = []
    page = 1
    while True:
        jobs = scrape_page(page)
        if not jobs:
            break
        all_jobs.extend(jobs)
        page += 1

    with open("jobs_talentmarket.json", "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"✅ scraped {len(all_jobs)} jobs total")

if __name__ == "__main__":
    main()

