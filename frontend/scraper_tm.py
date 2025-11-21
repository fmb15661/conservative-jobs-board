import json
import time
import requests
from bs4 import BeautifulSoup

LIST_URL = "https://talentmarket.org/jobs/"
OUTPUT = "public/jobs_talentmarket.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_org_from_detail(url):
    """Visit job detail page and extract the organization name."""
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # The organization name ALWAYS appears in the first paragraph(s)
        paragraphs = soup.select("p")
        for p in paragraphs:
            txt = p.get_text(" ", strip=True)

            # Look for patterns
            if txt.lower().startswith("about "):
                # example: "About Legal Insurrection Foundation"
                return txt.replace("About ", "").strip()

            if " is a " in txt:
                # example: "Do No Harm is a membership nonprofit..."
                return txt.split(" is a ")[0].strip()

            if " is an " in txt:
                # example: "Libertas Institute is an innovative..."
                return txt.split(" is an ")[0].strip()

        return "Talent Market"
    except:
        return "Talent Market"


def scrape_talent_market():
    print("Fetching Talent Market job list...")

    res = requests.get(LIST_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    cards = soup.select(".content-preview-card")
    print(f"Found {len(cards)} job cards")

    jobs = []

    for card in cards:
        try:
            # Title + link
            title_el = card.select_one("h2 a")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            url = title_el["href"]

            # Location
            loc_el = card.select_one(".location")
            location = loc_el.get_text(strip=True).replace("Location:", "").strip() if loc_el else "N/A"

            # Visit detail page for ORG name
            org = get_org_from_detail(url)

            job = {
                "title": title,
                "organization": org,
                "location": location,
                "url": url,
                "type": "N/A"
            }

            jobs.append(job)
            time.sleep(0.3)

        except Exception as e:
            print("Error parsing job:", e)
            continue

    # Save
    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Talent Market jobs to {OUTPUT}")


if __name__ == "__main__":
    scrape_talent_market()

