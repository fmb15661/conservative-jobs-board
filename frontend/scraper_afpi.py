from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import datetime
import time

def scrape_afpi_jobs():
    options = Options()

    # IMPORTANT: full browser mode (NOT HEADLESS)
    # Do NOT enable headless.
    # Cloudflare blocks headless browsers.
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    url = "https://americafirstpolicy.com/careers"
    driver.get(url)

    # Wait long enough for Cloudflare to pass
    time.sleep(10)

    # Scroll to bottom (forces JS to load jobs)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    jobs = []

    # Look for real job listing elements (we’ll refine once we see them)
    job_elements = driver.find_elements(By.CSS_SELECTOR, "a, div, li")

    # Temporary capture to inspect text
    for el in job_elements:
        text = el.text.strip()
        href = el.get_attribute("href")

        if "Apply" in text or "Job" in text or "Position" in text:
            print("FOUND ELEMENT:", text, href)

    # Dump full final DOM to file
    with open("frontend/public/afpi_after_cloudflare.html", "w") as f:
        f.write(driver.page_source)

    driver.quit()
    print("DONE. View afpi_after_cloudflare.html")


if __name__ == "__main__":
    scrape_afpi_jobs()

