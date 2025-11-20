import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

OUTPUT = "public/jobs_talentmarket.json"
BASE_URL = "https://talentmarket.org/job-openings/"

def scrape_talent_market():
    # Use visible Chrome so we can actually see what is happening.
    chrome_options = Options()
    # Do NOT run headless so you can watch it.
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    print("Launching Chrome…")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_jobs = []
    page = 1
    max_pages = 15  # safety cap so it doesn't loop forever

    while page <= max_pages:
        if page == 1:
            url = BASE_URL
        else:
            # IMPORTANT: correct pagination pattern
            url = f"{BASE_URL}page/{page}/"

        print(f"\nLoading page {page}: {url}")
        driver.get(url)
        time.sleep(3)

        # Scroll a few times to force JS to load all cards
        last_height = driver.execute_script("return document.body.scrollHeight")
        for _ in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
        print(f"Page {page}: found {len(cards)} cards")

        # If we hit a page with zero cards AFTER at least one good page, stop.
        if len(cards) == 0:
            if page == 1:
                print("No cards found on page 1 — site structure may have changed.")
            else:
                print("No more job pages detected — stopping.")
            break

        for card in cards:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "h2 a")
                title = title_el.text.strip()
                link = title_el.get_attribute("href").strip()

                # Location line like: "Location: Virtual"
                try:
                    loc_el = card.find_element(By.CSS_SELECTOR, ".location")
                    location_raw = loc_el.text.strip()
                    location = location_raw.replace("Location:", "").strip()
                except Exception:
                    location = "N/A"

                # Date line if present
                try:
                    date_el = card.find_element(By.CSS_SELECTOR, ".date")
                    date_posted = date_el.text.strip()
                except Exception:
                    date_posted = ""

                job = {
                    "title": title,
                    "organization": "Talent Market",
                    "location": location,
                    "type": "N/A",
                    "date_posted": date_posted,
                    "link": link
                }
                all_jobs.append(job)
            except Exception as e:
                print("Error parsing a job card:", e)
                continue

        page += 1

    driver.quit()

    print(f"\nTotal jobs collected: {len(all_jobs)}")

    with open(OUTPUT, "w") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Saved {len(all_jobs)} Talent Market jobs to {OUTPUT}")


if __name__ == "__main__":
    scrape_talent_market()

