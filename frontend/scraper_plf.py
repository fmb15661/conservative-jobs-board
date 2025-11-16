import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_plf_jobs():
    url = "https://www.pacificlegal.org/careers/"
    print("Requesting PLF careers page...")

    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    job_cards = soup.find_all("div", class_="career-item")

    print(f"Found {len(job_cards)} PLF job cards\n")

    for card in job_cards:
        # Title
        title_tag = card.find("h2")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Location (try preview-location first)
        loc_tag = card.select_one(".preview-location em")
        if loc_tag:
            location = loc_tag.get_text(strip=True)
        else:
            # fallback: first <p><em>
            p_em = card.find("p")
            if p_em and p_em.find("em"):
                location = p_em.find("em").get_text(strip=True)
            else:
                location = "N/A"

        # Apply Link
        apply_tag = card.find("a", class_="button")
        link = apply_tag["href"] if apply_tag else "N/A"

        job = {
            "title": title,
            "organization": "Pacific Legal Foundation",
            "location": location,
            "type": "N/A",
            "date_posted": "N/A",
            "link": link
        }

        print(f"Scraped job: {title} — {location}")
        jobs.append(job)

    # Save file
    output_path = os.path.join("public", "jobs_plf.json")
    with open(output_path, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"\nSaved {len(jobs)} PLF jobs to {output_path}")


if __name__ == "__main__":
    scrape_plf_jobs()

