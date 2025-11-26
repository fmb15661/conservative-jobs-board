import subprocess
import sys
import os

SCRAPER_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(SCRAPER_DIR, "..", "frontend", "public")

print("=== Running SCRAPERS/ folder scrapers ===")
print("Scraper dir:", SCRAPER_DIR)
print("Output directory:", PUBLIC_DIR, "\n")

FOLDER_SCRAPERS = [
    "scrape_ashbrook.py",
    "scrape_bri.py",
    "scrape_cato.py",
    "scrape_commonwealth.py",
    "scrape_fair.py",
    "scrape_fee.py",
    "scrape_fire.py",
    "scrape_heritage.py",
    "scrape_yaf_debug.py",
    "scraper_afpi.py",
    "scraper_cei.py",
    "scraper_claremont.py",
    "scraper_leadership_institute.py",
    "scraper_talentmarket_full.py",
    "scraper_talentmarket.py",
    "scraper_tm_selenium.py",
    "scraper_tppf.py",
    "scraper_yaf_selenium.py",
]

def run(script):
    print(f"--- Running {script} ---")
    path = os.path.join(SCRAPER_DIR, script)
    if not os.path.exists(path):
        print(f"❌ NOT FOUND: {script}\n")
        return
    try:
        subprocess.run([sys.executable, path], check=True)
        print(f"✓ Finished {script}\n")
    except Exception as e:
        print(f"✗ ERROR in {script}: {e}\n")

for script in FOLDER_SCRAPERS:
    run(script)

print("=== DONE: SCRAPERS/ folder scrapers ===")

