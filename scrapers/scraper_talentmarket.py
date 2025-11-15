import json
from requests_html import HTMLSession
from typing import List, Dict
from datetime import datetime


def scrape_talentmarket() -> List[Dict]:
    url = "https://talentmarket.org/job-openings/"
    jobs: List[Dict] = []

    session = HTMLSession()

    try:
        response = session.get(url, timeout=30)
        response.html.render(timeout=40)  # 👈 render JavaScript
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return jobs

    cards = response.html.find("div.content-preview-card")

    for card in cards:
        try:
            title_el = card.find("h2 a", first=True)
            title = title_el.text if title_el else "N/A"
            link = title_el.attrs["href"] if title_el else "N/A"

            org = "N/A"
            img = card.find("img", first=True)
            if img and "alt" in img.attrs:
                org = img.attrs["alt"].strip()

            loc_el = card.find("p.location", first=True)
            location = loc_el.text.replace("Location:", "").strip() if loc_el else "N/A"

            date_el = card.find("p.date", first=True)
            date_posted = date_el.text if date_el else datetime.today().strftime("%Y-%m-%d")

            jobs.append({
                "title": title,
                "organization": org,
                "location": location,
                "type": "N/A",
                "date_posted": date_posted,
                "link": link
            })
        except Exception as e:
            print(f"⚠️ Error parsing card: {e}")

    return jobs


def main():
    jobs = scrape_talentmarket()
    out_path = "jobs_talentmarket.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(jobs)} jobs to {out_path}")


if __name__ == "__main__":
    main()
