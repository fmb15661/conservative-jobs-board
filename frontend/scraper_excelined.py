import requests
from bs4 import BeautifulSoup
import json

def to_title_case(text):
    return " ".join(word.capitalize() for word in text.lower().split())

def scrape_excelined():
    url = "https://excelined.org/job-opportunities/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # ExcelinEd uses "the-resource resource-separator" blocks for each real job
    listings = soup.select(".the-resource.resource-separator")

    for listing in listings:
        left = listing.select_one(".resource-left")
        if not left:
            continue

        title_el = left.find("h1")
        link_el = left.find("a", href=True)

        if not title_el or not link_el:
            continue

        raw_title = title_el.get_text(strip=True)
        title = to_title_case(raw_title)

        url = link_el["href"]

        # ExcelinEd does not show location explicitly on listing blocks
        location = ""

        jobs.append({
            "title": title,
            "company": "ExcelinEd (Foundation for Excellence in Education)",
            "location": location,
            "url": url,
            "type": ""
        })

    # Write JSON
    with open("public/jobs_excelined.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("ExcelinEd jobs saved to public/jobs_excelined.json")

scrape_excelined()

