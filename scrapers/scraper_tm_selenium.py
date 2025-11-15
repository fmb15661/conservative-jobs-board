from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time, json, requests, re

BASE = "https://talentmarket.org/job-openings/"
OUTPUT = "frontend/public/jobs_talentmarket.json"
all_jobs = []

def get_driver():
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--disable-gpu")
    o.add_argument("--no-sandbox")
    o.add_argument("--window-size=1280,800")
    return webdriver.Chrome(options=o)

def extract_tm_org(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        s = BeautifulSoup(r.text, "lxml")
        title_el = s.find("h1")
        if not title_el:
            return "Unknown"
        next_p = title_el.find_next("p")
        if not next_p:
            return "Unknown"

        txt = next_p.get_text(" ", strip=True)
        txt = txt.replace("Organization:", "").replace("Role:", "").strip()

        # remove trailing location words
        txt = re.sub(r"\s+(Virtual|New Haven, CT|Washington, DC|Arlington, VA|Chicago, IL|Los Angeles, CA|honolulu, HI|Grand Rapids, MI)$","",txt,flags=re.IGNORECASE)

        # remove trailing state style patterns like ", XX"
        txt = re.sub(r",\s*[A-Z][A-Z]$","",txt)

        # final cleanup
        txt = re.sub(r"\s+$","",txt)
        return txt if txt else "Unknown"
    except:
        return "Unknown"

def clean_location(raw):
    if not raw:
        return "N/A"
    t = raw.get_text(" ", strip=True)
    t = t.replace("Location:", "").strip()
    return t if t else "N/A"

def scrape():
    d = get_driver()
    d.get(BASE)
    time.sleep(3)
    seen=set()
    while True:
        soup = BeautifulSoup(d.page_source,"lxml")
        cards = soup.select(".content-preview-card")
        for c in cards:
            a = c.select_one("h2 a")
            if not a or not a.get("href"): continue
            link = a["href"].strip()
            title = a.get_text(strip=True)
            if link in seen: continue
            seen.add(link)
            loc_el = c.select_one("p.location")
            date_el = c.select_one("p.date")
            org = extract_tm_org(link)
            all_jobs.append({
                "title": title,
                "organization": org,
                "location": clean_location(loc_el),
                "type":"N/A",
                "date_posted": date_el.get_text(strip=True) if date_el else "1970-01-01",
                "link": link
            })
        nxt = soup.find("a", string=lambda x:x and "Next" in x)
        if not nxt or not nxt.get("href"): break
        d.get(nxt["href"])
        time.sleep(2)
    d.quit()

if __name__=="__main__":
    scrape()
    with open(OUTPUT,"w") as f:
        json.dump(all_jobs,f,indent=2)
    print(f"✅ scraped",len(all_jobs),"jobs →",OUTPUT)

