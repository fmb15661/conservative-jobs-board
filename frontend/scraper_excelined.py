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

    # Each job appears inside a div with class "resource-left"
    listings = soup.select(".resource-left")

    for job in listings:
        title_el = job.find("h1")
        desc_el = job.find("p")
        link_el = job.find("a", href=True)

        if not title_el or not link_el:
            continue

        raw_title = title_el.get_text(strip=True)
        title = to_title_case(raw_title)

        url = link_el["href"]

        # ExcelinEd does not clearly list city/state in HTML
        # So location is blank unless later we add manual entry
        location = ""

        jobs.append({
            "title": title,
            "company": "ExcelinEd (Foundation for Excellence in Education)",
            "location": location,
            "url": url,      # Their own job page – correct
            "type": ""       # You fill manually later
        })

    # Save file
    with open("public/jobs_excelined.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("ExcelinEd jobs saved to public/jobs_excelined.json")

scrape_excelined()

