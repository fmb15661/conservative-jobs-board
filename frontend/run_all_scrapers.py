import os
import subprocess

# All scraper filenames in frontend/
SCRAPERS = [
    "scraper_tm_selenium.py",
    "scraper_acton.py",
    "scraper_aier.py",
    "scraper_afpi.py",
    "scraper_aei.py",
    "scraper_cato.py",
    "scraper_cei.py",
    "scraper_claremont.py",
    "scraper_crc.py",
    "scraper_excelined.py",
    "scraper_heritage.py",
    "scraper_hudson.py",
    "scraper_leadership_institute.py",
    "scraper_ntu.py",
    "scraper_plf.py",
    "scraper_talentmarket.py",
    "scraper_yaf.py",
    "scraper_alec.py",
    "scraper_acc.py",
]

def run_scrapers():
    base = os.getcwd()

    print("\n=== Running ALL Job Scrapers ===\n")

    for script in SCRAPERS:
        path = os.path.join(base, script)
        if os.path.exists(path):
            print(f"\n--- Running {script} ---")
            try:
                subprocess.run(["python3", path], check=False)
            except Exception as e:
                print(f"Error running {script}: {e}")
        else:
            print(f"Skipping {script} (not found)")

    print("\n=== ALL SCRAPERS FINISHED ===\n")

if __name__ == "__main__":
    run_scrapers()

