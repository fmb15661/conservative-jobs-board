import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://excelined.org/job-opportunities/"

def scrape_excelined():
    response = requests.get(BASE_URL, timeout=15)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Find the container with all job postings
    job_blocks = soup.select(".the-resource")

    for block in job_blocks:
        title_el = block.select_one("h1")
        link_el = block.select_one("a[href]")

        if not title_el or not link_el:
            continue

        title = title_el.get_text(strip=True)
        url = link_el["href"]
        company = "ExcelinEd (Foundation for Excellence in Education)"

        # Step 1: fetch job detail page to extract description
        desc_text = ""
        try:
            job_detail = requests.get(url, timeout=15)
            detail_soup = BeautifulSoup(job_detail.text, "html.parser")

            # Gutenberg content container
            desc_container = detail_soup.select_one(".gutenberg")
            if desc_container:
                desc_text = desc_container.get_text(" ", strip=True)
        except:
            pass

        jobs.append({
            "title": title,
            "company": company,
            "location": "",   # will be handled by UI
            "url": url,
            "type": "",
            "description": desc_text   # NEW FIELD
        })

    # Save JSON
    with open("public/jobs_excelined.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print("ExcelinEd jobs saved to public/jobs_excelined.json")

if __name__ == "__main__":
    scrape_excelined()

