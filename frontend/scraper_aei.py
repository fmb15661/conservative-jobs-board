import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_aei_jobs():
    url = "https://careers-aei.icims.com/jobs/search?in_iframe=1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://careers-aei.icims.com",
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print("FAILED TO LOAD AEI PAGE:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    jobs_output = []

    job_blocks = soup.find_all("div", class_="row")

    for job in job_blocks:
        title_tag = job.find("h3")
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)

        link_tag = job.find("a", {"class": "iCIMS_Anchor"})
        url = link_tag["href"] if link_tag else ""

        loc_tag = job.find("span", class_="sr-only", string="Job Locations")
        location = "N/A"
        if loc_tag:
            loc_span = loc_tag.find_next("span")
            if loc_span:
                location = loc_span.get_text(strip=True)

        desc_tag = job.find("div", class_="description")
        desc_text = desc_tag.get_text(" ", strip=True).lower() if desc_tag else ""

        # --- Virtual detection ---
        loc_lower = location.lower()
        if "virtual" in loc_lower or "virtual" in desc_text:
            location = "Virtual"

        job_data = {
            "title": title,
            "company": "American Enterprise Institute",
            "location": location if location else "N/A",
            "url": url,
            "type": "N/A"
        }

        jobs_output.append(job_data)

    with open("frontend/public/jobs_aei.json", "w") as f:
        json.dump(jobs_output, f, indent=2)

    print(f"AEI scraping complete — {len(jobs_output)} jobs saved.")


if __name__ == "__main__":
    scrape_aei_jobs()

