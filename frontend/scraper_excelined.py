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

    # This matches EXACTLY the structure you pasted
    listings = soup.select("div.the-resource.resource-separator")

    for listing in listings:
        left = listing.select_one("div.resource-left")
        if not left:
            continue

        # Title
        title_el = left.find("h1")
        if not title_el:
            continue

        raw_title = title_el.get_text(strip=True)
        title = to_title_case(raw_title)

        # Job URL is the FIRST <a> inside resource-left
        link_el = left.find("a", href=True)
        if not link_el:
            continue

        job_url = link_el["href"]

        # ExcelinEd does not provide a location field
        location = ""

        jobs.append({
            "title": title,
            "company": "ExcelinEd (Foundation for Excellence in Education)",
            "location": location,
            "url": job_url,
            "type": ""
        })

    with open("public/jobs_excelined.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("ExcelinEd jobs saved to public/jobs_excelined.json")

scrape_excelined()

