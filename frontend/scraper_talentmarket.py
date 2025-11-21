import requests
import json

OUTPUT = "public/jobs_talentmarket.json"

API_URL = "https://talentmarket.org/wp-json/wp/v2/jobs/?per_page=100"

def scrape_talent_market():
    print("Fetching Talent Market jobs from WordPress REST API...")

    try:
        response = requests.get(API_URL, timeout=20)
        response.raise_for_status()
        posts = response.json()
    except Exception as e:
        print("Error fetching API:", e)
        return

    jobs = []

    for post in posts:
        try:
            title = post["title"]["rendered"].strip()
            link = post["link"].strip()

            # Extract fields
            acf = post.get("acf", {})
            location = acf.get("location", "N/A")
            date_posted = post.get("date", "").split("T")[0]

            job = {
                "title": title,
                "organization": "Talent Market",
                "location": location,
                "type": "N/A",
                "url": link
            }

            jobs.append(job)

        except Exception as e:
            print("Error parsing job:", e)
            continue

    # Save output
    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Talent Market jobs to {OUTPUT}")


if __name__ == "__main__":
    scrape_talent_market()

