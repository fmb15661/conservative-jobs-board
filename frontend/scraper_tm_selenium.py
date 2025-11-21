import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

OUTPUT = "public/jobs_talentmarket.json"


# -------------------------
# SET UP SELENIUM BROWSER
# -------------------------
def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("detach", True)  # Keep window open

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    return driver


# -----------------------------------------
# GET ALL LISTING PAGES (page/1 to page/99)
# -----------------------------------------
def get_listing_pages(driver):
    pages = []
    for i in range(1, 50):  # 50 is safe upper bound
        url = f"https://talentmarket.org/job-openings/page/{i}/"
        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
        if len(cards) == 0:
            break

        pages.append(url)

    return pages


# ---------------------------------------------------
# EXTRACT JOB TITLE + LINK FROM LISTING PAGE CARDS
# ---------------------------------------------------
def extract_jobs_from_listing_page(driver):
    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
    for card in cards:
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_el.text.strip()
            link = title_el.get_attribute("href").strip()

            jobs.append({
                "title": title,
                "url": link
            })

        except Exception:
            continue

    return jobs


# ---------------------------------------------------
# VISIT EACH JOB DETAIL PAGE TO GET TRUE ORG + LOC
# ---------------------------------------------------
def scrape_detail_page(driver, job_url):
    driver.get(job_url)
    time.sleep(2)

    try:
        about = driver.find_element(By.CSS_SELECTOR, "p.article-about").text.strip().split("\n")
        org = about[0].strip()
        location = about[1].strip() if len(about) > 1 else "N/A"

        return org, location

    except Exception:
        return "N/A", "N/A"


# -------------------------
# MAIN SCRAPER
# -------------------------
def scrape_talent_market():
    driver = start_browser()
    print("\n=== TALENT MARKET SCRAPER STARTED ===\n")

    print("Discovering listing pages...")
    listing_pages = get_listing_pages(driver)
    print(f"Found {len(listing_pages)} pages\n")

    # Collect listing-level jobs (title + link)
    found_jobs = []
    seen_urls = set()

    for page_url in listing_pages:
        print(f"Scraping listing page: {page_url}")
        driver.get(page_url)
        time.sleep(2)

        listing_jobs = extract_jobs_from_listing_page(driver)
        for j in listing_jobs:
            if j["url"] not in seen_urls:
                found_jobs.append(j)
                seen_urls.add(j["url"])

    print(f"\nCollected {len(found_jobs)} jobs from listings")
    print("Now scraping each job's detail page...\n")

    final_jobs = []

    for j in found_jobs:
        try:
            org, location = scrape_detail_page(driver, j["url"])
            job = {
                "title": j["title"],
                "organization": org,
                "location": location,
                "url": j["url"],
                "type": "N/A"
            }
            final_jobs.append(job)
            print(f"✓ {j['title']} — {org}")

        except Exception as e:
            print(f"Error on {j['url']}: {e}")

    driver.quit()

    # Write output
    with open(OUTPUT, "w") as f:
        json.dump(final_jobs, f, indent=2)

    print(f"\nSaved {len(final_jobs)} jobs → {OUTPUT}")
    print("\n=== DONE ===\n")


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    scrape_talent_market()

