from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import os

def scrape_bri():
    org = "Bill of Rights Institute"
    url = "https://billofrightsinstitute.org/about-bri/join-our-team"

    print(f"Scraping {org} (JavaScript-rendered page)…")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    # EACH JOB CARD
    cards = soup.select("div.mb-20.border.rounded")

    for card in cards:
        # Title
        title_tag = card.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Location
        loc_tag = card.find("span", string=lambda t: t and "Location:" in t)
        location = loc_tag.parent.get_text(strip=True).replace("Location:", "").strip() if loc_tag else "N/A"

        # URL → no URL in markup, use page URL as fallback
        job_url = url

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": job_url
        })

    # Save JSON
    output_path = os.path.join(
        os.path.dirname(__file__),
        "../frontend/public/jobs_bri.json"
    )
    output_path = os.path.abspath(output_path)

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} BRI job(s) to {output_path}")

if __name__ == "__main__":
    scrape_bri()

