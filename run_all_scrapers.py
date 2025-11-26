import subprocess
import sys
import os

# === Correct project base directory ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# === Correct output directory (React public folder) ===
PUBLIC_DIR = os.path.join(BASE_DIR, "frontend", "public")

print("Running ALL scrapers...")
print("Scraper directory:", BASE_DIR)
print("Output directory:", PUBLIC_DIR, "\n")

def run(script):
    path = os.path.join(BASE_DIR, script)

    print(f"--- Running {script} ---")

    if not os.path.exists(path):
        print(f"❌ NOT FOUND: {script}\n")
        return

    try:
        subprocess.run([sys.executable, path], check=True)
        print(f"✓ Finished {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR in {script}: {e}\n")

# === FULL LIST OF SCRAPERS ===
SCRAPERS = [
    "scraper_talentmarket.py",
    "scraper_yaf_selenium.py",
    "scraper_afpi.py",
    "scraper_hudson.py",
    "scraper_cato.py",
    "scraper_plf.py",
    "scraper_ntu.py",
    "scraper_acton.py",
    "scraper_aier.py",
    "scraper_excelined.py",
    "scraper_claremont.py",
    "scraper_heritage.py",
    "scraper_cei.py",
    "scraper_tppf.py",
    "scraper_leadership_institute.py",
    "scraper_crc.py",
    "scraper_alec.py",
    "scraper_acc.py",
    "scraper_amprinproj.py",
    "scrape_ashbrook.py",
    "scrape_bri.py",
    "scrape_commonwealth.py",
    "scrape_fee.py",
    "scrape_fire.py",
]

for script in SCRAPERS:
    run(script)

print("\n=== ALL SCRAPERS COMPLETE ===")

