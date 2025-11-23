import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_ashbrook():
    url = "https://ashbrook.org/jobs/"
    org = "Ashbrook Center"

    print(f"Scraping {org}...")

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    # Jobs are inside <div class="m-content"> <p><a>...</a> (Remote)</p>
    content_blocks = soup.select(".m-content p")

    for block in content_blocks:
        link = block.find("a")
        if not link:
            continue

        title = link.get_text(strip=True)
        job_url = link["href"]

        # make URLs absolute
        if job_url.startswith("/"):
            job_url = "https://ashbrook.org" + job_url

        # try to extract location from the rest of the <p> tag
        full_text = block.get_text(" ", strip=True)
        location = "N/A"

        # detect parentheses like "(Remote)"
        if "(" in full_text and ")" in full_text:
            try:
                location = full_text.split("(")[1].split(")")[0].strip()
            except:
                pass

        jobs.append({
            "title": title,
            "organization": org,
            "location": location,
            "url": job_url
        })

    # Write JSON to frontend/public
    output_path = os.path.join(
        os.path.dirname(__file__),
        "../frontend/public/jobs_ashbrook.json"
    )
    output_path = os.path.abspath(output_path)

    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Ashbrook job(s) to {output_path}")


if __name__ == "__main__":
    scrape_ashbrook()

