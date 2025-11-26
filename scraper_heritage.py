import requests
import json

API_URL = "https://careers-aei.icims.com/jobs/search?pr=0&schema=1&format=json"
OUTPUT = "public/jobs_heritage.json"

def scrape_heritage():
    print("Requesting Heritage ICIMS JSON API...")

    response = requests.get(API_URL, headers={
        "User-Agent": "Mozilla/5.0"
    })

    if not response.ok:
        print("❌ Failed to load API:", response.status_code)
        return

    data = response.json()

    jobs = []
    for item in data.get("jobs", []):
        title = item.get("title", "N/A")
        link = item.get("url", "N/A")
        location = item.get("location", "Virtual")

        jobs.append({
            "title": title,
            "organization": "Heritage Foundation",
            "location": location,
            "type": "N/A",
            "link": link
        })

    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)

    print(f"Saved {len(jobs)} Heritage jobs to {OUTPUT}")

if __name__ == "__main__":
    scrape_heritage()

