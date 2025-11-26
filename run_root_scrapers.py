import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "frontend", "public")

print("=== Running ROOT (top-level) scrapers ===")
print("Root directory:", BASE_DIR)
print("Output directory:", PUBLIC_DIR, "\n")

ROOT_SCRAPERS = [
    "scraper_acc.py",
    "scraper_acton.py",
    "scraper_aei.py",
    "scraper_aier.py",
    "scraper_alec.py",
    "scraper_amprinproj.py",
    "scraper_app.py",
    "scraper_cato.py",
    "scraper_crc.py",
    "scraper_excelined.py",
    "scraper_heritage.py",
    "scraper_hudson.py",
    "scraper_ntu.py",
    "scraper_plf.py",
    "scraper_tm.py",
]

def run(script):
    print(f"--- Running {script} ---")
    path = os.path.join(BASE_DIR, script)
    if not os.path.exists(path):
        print(f"❌ NOT FOUND: {script}\n")
        return
    try:
        subprocess.run([sys.executable, path], check=True)
        print(f"✓ Finished {script}\n")
    except Exception as e:
        print(f"✗ ERROR in {script}: {e}\n")

for script in ROOT_SCRAPERS:
    run(script)

print("=== DONE: ROOT SCRAPERS ===")

