import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://talentmarket.org/job-openings/page/{}/"
OUTPUT = "public/jobs_talentmarket.json"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1400,2500")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def scroll(driver):
    """Make sure lazy-loaded elements appear."""
    last = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
        new = driver.execute_script("return document.body.scrollHeight")
        if new == last:
            return
        last = new


def collect_listing_urls(driver):
    """Collect all job URLs from all pages WITHOUT entering any job page."""
    urls = []

    page = 1
    while True:
        url = BASE_URL.format(page)
        print(f"\nLoading page {page}: {url}")

        driver.get(url)
        time.sleep(1.5)
        scroll(driver)

        cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
        print(f"Page {page}: found {len(cards)} cards")

        if len(cards) == 0:
            break

        for card in cards:
            try:
                a = card.find_element(By.CSS_SELECTOR, "h2 a")
                urls.append(a.get_attribute("href"))
            except:
                continue

        page += 1

    print(f"\nCollected {len(urls)} job URLs.")
    return urls


def scrape_detail(driver, url):
    """Scrape a detail job page for organization + location."""
    try:
        driver.get(url)
        time.sleep(1.2)
        scroll(driver)

        about = driver.find_element(By.CSS_SELECTOR, "p.article-about").text.strip()
        lines = [x.strip() for x in about.split("\n") if x.strip()]
        org = lines[0] if len(lines) > 0 else "N/A"
        location = lines[1] if len(lines) > 1 else "N/A"

        title = driver.find_element(By.CSS_SELECTOR, "h1.article-h1").text.strip()

        return {
            "title": title,
            "organization": org,
            "location": location,
            "url": url,
            "type": "N/A"
        }

    except Exception as e:
        print("Detail scrape error:", e)
        return None


def scrape_talent_market():
    driver = get_driver()

    # STEP 1: Collect all job URLs safely
    job_urls = collect_listing_urls(driver)

    jobs = []

    # STEP 2: Visit each job page independently
    for url in job_urls:
        print(f"Scraping detail: {url}")
        job = scrape_detail(driver, url)
        if job:
            jobs.append(job)

    driver.quit()

    print(f"\nTotal jobs scraped: {len(jobs)}")
    with open(OUTPUT, "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"Saved {len(jobs)} → {OUTPUT}")


if __name__ == "__main__":
    scrape_talent_market()

