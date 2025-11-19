import requests
from bs4 import BeautifulSoup
import json

AEI_URL = "https://careers-aei.icims.com/jobs/search?in_iframe=1"

def scrape_aei():
    print("Scraping AEI…")

    jobs = []

    # pull the iCIMS iframe source directly
    r = requests.get(AEI_URL, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    # each job listing is in a "div.row" block
    listings = soup.select("div.row")

    for block in listings:
        # Title
        title_el = block.select_one("h3")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)

        # Link
        link_el = block.select_one("a.iCIMS_Anchor")
        if not link_el:
            continue

        url = link_el.get("href")
        if url.startswith("/"):
            url = "https://careers-aei.icims.com" + url

        # Location
        loc_el = block.select_one(".header.left span:not(.sr-only)")
        location = ""

        if loc_el:
            location = loc_el.get_text(strip=True)
        else:
            location = ""

        # Standardized JSON format
        job = {
            "title": title,
            "company": "American Enterprise Institute",
            "location": location,
            "url": url,
            "type": "N/A"
        }

        jobs.append(job)

    # save results
    with open("public/jobs_aei.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("AEI jobs saved → public/jobs_aei.json")

if __name__ == "__main__":
    scrape_aei()

