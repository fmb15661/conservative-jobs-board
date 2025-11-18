import requests
from bs4 import BeautifulSoup
import json

# Convert ALL CAPS to Title Case (consistent with Acton rule)
def to_title_case(text):
    return " ".join([word.capitalize() for word in text.lower().split()])

def scrape_aier():
    url = "https://talentmarket.org/job-listings/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    listings = soup.select(".wpjb-job")

    for job in listings:
        org = job.select_one(".wpjb-job-company")
        if not org:
            continue

        org_name = org.get_text(strip=True)

        # Only capture AIER jobs
        if "aier" in org_name.lower() or "american institute for economic research" in org_name.lower():

            title_el = job.select_one(".wpjb-job-title a")
            loc_el = job.select_one(".wpjb-job-location")

            if not title_el:
                continue

            raw_title = title_el.get_text(strip=True)
            title = to_title_case(raw_title)

            location = loc_el.get_text(strip=True) if loc_el else ""

            # RULE: ALWAYS link to AIER homepage
            aier_link = "https://www.aier.org/careers/"

            jobs.append({
                "title": title,
                "company": "American Institute for Economic Research (AIER)",
                "location": location,
                "url": aier_link,
                "type": ""   # filled manually later
            })

    with open("public/jobs_aier.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("AIER jobs saved to public/jobs_aier.json")

scrape_aier()

