import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://talentmarket.org/job-openings/page/{}/"
OUTPUT = "public/jobs_talentmarket.json"


def scrape_talent_market():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1400,1000")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    all_jobs = []

    for page in range(1, 20):
        url = BASE_URL.format(page)
        print(f"\nLoading page {page}: {url}")

        driver.get(url)
        time.sleep(2)

        # Scroll to ensure all JS content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
        print(f"Page {page}: found {len(cards)} cards")

        if len(cards) == 0:
            print("Stopping — empty page.")
            break

        for i in range(len(cards)):
            try:
                card = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")[i]

                title_el = card.find_element(By.CSS_SELECTOR, "h2 a")
                title = title_el.text.strip()
                url = title_el.get_attribute("href")

                loc_el = card.find_element(By.CSS_SELECTOR, ".location")
                location = loc_el.text.replace("Location:", "").strip()

                desc_text = card.text
                organization = extract_org(desc_text)

                job = {
                    "title": title,
                    "organization": organization,
                    "location": location,
                    "url": url,
                    "type": "N/A"
                }

                all_jobs.append(job)

            except Exception as e:
                print("Error parsing job:", e)
                continue

    driver.quit()

    print(f"\nTotal jobs collected: {len(all_jobs)}")
    with open(OUTPUT, "w") as f:
        json.dump(all_jobs, f, indent=2)
    print(f"Saved {len(all_jobs)} jobs → {OUTPUT}")


def extract_org(text):
    # Detect "About X" pattern
    if "About " in text:
        fragment = text.split("About ")[1]
        words = fragment.split(" ")[:4]
        cleaned = " ".join(w.strip(",.:") for w in words)
        return cleaned

    return "N/A"


if __name__ == "__main__":
    scrape_talent_market()

