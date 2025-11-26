import os
import subprocess

# Always run scrapers from the project root (THIS restores original behavior)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRAPERS_DIR = os.path.join(PROJECT_ROOT, "scrapers")

print("\n=== Running ALL scrapers exactly like before ===")
print(f"Project root: {PROJECT_ROOT}")
print(f"Scrapers folder: {SCRAPERS_DIR}\n")

# All scrapers that lived in /scrapers originally
SCRAPER_FILES = [
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

# These 3 MUST run inside the scrapers directory because their code expects it
LEGACY_PATH_SCRAPERS = {
    "scrape_fee.py",
    "scrape_fire.py",
    "scrape_heritage.py",
}

for scraper in SCRAPER_FILES:
    scraper_path = os.path.join(SCRAPERS_DIR, scraper)

    if not os.path.exists(scraper_path):
        print(f"❌ Missing scraper: {scraper}")
        continue

    # Determine where to run this scraper from
    if scraper in LEGACY_PATH_SCRAPERS:
        run_dir = SCRAPERS_DIR
    else:
        run_dir = PROJECT_ROOT

    print(f"\n--- Running {scraper} (cwd={run_dir}) ---")

    try:
        subprocess.run(["python3", scraper_path], check=True, cwd=run_dir)
        print(f"✓ Finished {scraper}")
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR in {scraper}: {e}")

print("\n=== DONE: all scrapers run exactly like before ===\n")

