import requests
import json

def scrape_hudson_jobs():
    url = "https://recruiting.paylocity.com/recruiting/api/v2/companies/20837/jobs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept": "application/json",
    }

    print("Requesting Hudson job list from Paylocity API...")

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    try:
        data = response.json()
    except:
        print("❌ API did not return JSON. Dumping response text:")
        print(response.text[:1000])
        return []

    print(f"Found {len(data)} jobs from API")

    jobs = []
    for job in data:
        title = job.get("title", "N/A")
        job_id = job.get("id")
        location = job.get("city", "N/A")
        state = job.get("state", "")

        if state:
            location = f"{location}, {state}"

        # Construct job details page URL
        link = f"https://recruiting.paylocity.com/recruiting/jobs/Details/{job_id}/HUDSON-INSTITUTE-INC"

        jobs.append({
            "title": title,
            "organization": "Hudson Institute",
            "location": location,
            "type": "N/A",
            "date_posted": job.get("createdDate", "N/A"),
            "link": link
        })

    return jobs


if __name__ == "__main__":
    all_jobs = scrape_hudson_jobs()

    output_path = "public/jobs_hudson.json"
    with open(output_path, "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"\nScraped {len(all_jobs)} Hudson jobs and saved to {output_path}")

