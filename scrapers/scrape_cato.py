from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import json
import os

def scrape_cato():
    org = "Cato Institute"
    base_url = "https://recruiting.paylocity.com"
    paylocity_url = (
        "https://recruiting.paylocity.com/recruiting/jobs/All/"
        "eb1d479c-5f1a-41bf-8916-c72467c0b7ca/Cato-Institute?wmode=transparent&auto=1"
    )

    print("Scraping Cato Institute from Paylocity…")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(paylocity_url, wait_until="domcontentloaded")

        # Wait for the job rows to load inside the Paylocity page
        try:
            page.wait_for_selector("div.row.job-listing-job-item", timeout=10000)
        except PlaywrightTimeoutError:
            print("Timed out waiting for job items on Paylocity page.")
        
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    # Each job row looks like:
    # <div class="row job-listing-job-item"> ... </div>
    cards = soup.select("div.row.job-listing-job-item")

    for card in cards:
        # Title
        title_tag = card.select_one(".job-item-title a")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # URL (make absolute)
        link = title_tag["href"] if title_tag else ""
        if link.startswith("/"):
            link = base_url + link

        # Location
        loc_tag = card.select_one(".location-column span.job-item-normal")
        location = loc_tag.get_text(strip=True) if loc_tag else ""

        # 🔧 Simple display fix: normalize this specific location text
        if location == "Hybrid - Cato Institute Headquarters":
            location = "Hybrid/Washington, D.C."

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": link
        })

    # Save to frontend/public/jobs_cato.json
    output_path = os.path.join(
        os.path.dirname(__file__),
        "../frontend/public/jobs_cato.json"
    )
    output_path = os.path.abspath(output_path)

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Cato job(s) to {output_path}")


if __name__ == "__main__":
    scrape_cato()

