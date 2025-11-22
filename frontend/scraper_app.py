import json
import requests
from bs4 import BeautifulSoup

URL = "https://americanprinciplesproject.org/careers/"
OUTPUT = "public/jobs_app.json"


def scrape_app():
    print("Fetching APP job postings...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    resp = requests.get(URL, headers=headers, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")

    main = soup.find("div", id="main-careers")
    if not main:
        print("Could not find main careers container on APP page.")
        jobs = []
    else:
        jobs = []
        # Each job is introduced by an <h2> title
        for h2 in main.find_all("h2"):
            title = h2.get_text(strip=True)
            if not title:
                continue

            # Find the location line in the paragraphs following this h2
            location = "N/A"
            for sib in h2.find_all_next(["p", "h2", "h3", "hr"]):
                # Stop when we reach the next job/section
                if sib is not h2 and sib.name in ["h2", "h3", "hr"]:
                    break
                if sib.name == "p":
                    text = sib.get_text(" ", strip=True)
                    if "Location:" in text:
                        location = text.split("Location:", 1)[1].strip()
                        break

            job = {
                "title": title,
                "organization": "American Principles Project",
                "location": location,
                "type": "N/A",
                "link": URL,
            }
            jobs.append(job)

    print(f"Found {len(jobs)} APP jobs")
    # Make sure the output directory exists and write JSON
    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    scrape_app()

