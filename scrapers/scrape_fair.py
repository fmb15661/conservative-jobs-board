from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from bs4 import BeautifulSoup
import json
import os

def scrape_fair():
    org = "Federation for American Immigration Reform (FAIR)"
    url = "https://www.fairus.org/about-fair/career-opportunities"

    print("Scraping FAIR (Cloudflare-protected, using real browser)…")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except PlaywrightTimeoutError:
            print("Timeout loading FAIR page — Cloudflare may be slowing load.")

        # Allow Cloudflare time to finish JS challenges
        page.wait_for_timeout(7000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")

    jobs = []

    # All FAIR job titles appear as <h3> within the "Full-Time Positions" section
    for h3 in soup.select("h3"):
        title = h3.get_text(strip=True)

        # Skip headers that are not job titles
        if "Full-Time" in title or "Positions" in title or "Mission" in title:
            continue

        # Next paragraph holds location (bold text)
        p = h3.find_next_sibling("p")
        if not p:
            continue
        raw_loc = p.get_text(strip=True)

        # Normalize location format
        location = ""
        if "Washington" in raw_loc or "D.C." in raw_loc:
            location = "Hybrid/Washington, D.C."

        # Find the first <a> link under this job block
        link_tag = h3.find_next("a")
        link = link_tag["href"] if link_tag and link_tag.has_attr("href") else ""

        if link.startswith("/"):
            link = "https://www.fairus.org" + link

        # Only add if we have a title and location
        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": link
        })

    # Save jobs
    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../frontend/public/jobs_fair.json")
    )

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} FAIR job(s) to {output_path}")


if __name__ == "__main__":
    scrape_fair()

