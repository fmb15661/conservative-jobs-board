from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time, json
import requests
from bs4 import BeautifulSoup

BASE = "https://talentmarket.org/job-openings/"
jobs = []

def get_org(link):
    try:
        html = requests.get(link, headers={"User-Agent":"Mozilla/5.0"}).text
        soup = BeautifulSoup(html, "html.parser")
        h2 = soup.find("h2")
        if not h2:
            return "Unknown Organization"
        txt = h2.get_text(strip=True)
        if "About the " in txt:
            return txt.replace("About the","").strip()
        return txt
    except:
        return "Unknown Organization"

def scrape_all_pages():
    options = Options()
    options.add_argument("--headless=new")

    # correct selenium syntax
    driver = webdriver.Chrome(options=options)

    page = 1
    while True:
        url = BASE if page == 1 else f"{BASE}page/{page}/"
        driver.get(url)
        time.sleep(2)

        cards = driver.find_elements(By.CSS_SELECTOR, ".content-preview-card")
        if not cards:
            break

        for card in cards:
            link_el = card.find_element(By.CSS_SELECTOR, "h2 a")
            title = link_el.text.strip()
            link  = link_el.get_attribute("href").strip()

            loc_el = card.find_element(By.CSS_SELECTOR, ".location")
            loc = loc_el.getText() if hasattr(loc_el,'getText') else loc_el.text
            loc = loc.replace("Location:","").strip()

            date_el = card.find_element(By.CSS_SELECTOR, ".date")
            date = date_el.text.strip()

            org = get_org(link)

            jobs.append({
                "title": title,
                "organization": org,
                "location": loc,
                "type": "N/A",
                "date_posted": date,
                "link": link
            })

        page += 1

    driver.quit()

def main():
    scrape_all_pages()
    out = []
    import datetime
    for j in jobs:
        try:
            dt = datetime.datetime.strptime(j["date_posted"], "%B %d, %Y")
            j["date_posted"] = dt.strftime("%Y-%m-%d")
        except:
            pass
        out.append(j)

    with open("frontend/public/jobs_talentmarket.json","w") as f:
        json.dump(out, f, indent=2)

    print(f"✅ Saved {len(out)} jobs to jobs_talentmarket.json")

main()

