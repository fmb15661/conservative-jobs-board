import requests
from bs4 import BeautifulSoup
import json

def scrape_ntu():
    url = "https://www.ntu.org/about/page/career-and-internship-opportunities"
    print("Requesting NTU careers page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Where NTU lists the jobs
    job_blocks = soup.select("div.career__content a")

    jobs = []

    for a in job_blocks:
        title_raw = a.get_text(strip=True)
        link = a.get("href")

        # Absolute URL
        if link.startswith("/"):
            link = "https://www.ntu.org" + link

        # LOAD DETAIL PAGE to get location
        loc = "N/A"
        try:
            detail = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
            detail.raise_for_status()
            s2 = BeautifulSoup(detail.text, "html.parser")

            # ApplyToJob uses <div class="posting-categories"> for location
            loc_el = s2.select_one(".posting-categories div")
            if loc_el:
                loc = loc_el.get_text(strip=True)
        except:
            pass

        # CLEAN title (remove salary prefixes like “Vice President of Ops - Salary Range …”)
        title = title_raw.split(" - Salary Range")[0].strip()

        jobs.append({
            "title": title,
            "organization": "National Taxpayers Union",
            "location": loc,
            "type": "N/A",
            # no date_posted (you removed this globally)
            "link": link
        })

    # Save JSON
    with open("public/jobs_ntu.json", "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} NTU jobs to public/jobs_ntu.json")

if __name__ == "__main__":
    scrape_ntu()

