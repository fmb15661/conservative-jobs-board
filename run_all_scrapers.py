import os
import subprocess
import sys

SCRAPER_DIR = "scrapers"

def run_scraper(scraper_path):
    print(f"▶️ Running {scraper_path} ...")
    result = subprocess.run(
        [sys.executable, scraper_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    # Print standard output
    if result.stdout:
        print(result.stdout)
    # Print any errors
    if result.stderr:
        print("⚠️ Errors:")
        print(result.stderr)
    print("----------------------------------------------------")

def main():
    print("=========================================")
    print("     CONSERVATIVE JOBS BOARD SCRAPERS    ")
    print("=========================================\n")

    # Look for all scraper_*.py files in scrapers/ folder
    if not os.path.isdir(SCRAPER_DIR):
        print(f"❌ Folder '{SCRAPER_DIR}' not found.")
        return

    files = sorted(os.listdir(SCRAPER_DIR))
    scrapers = [f for f in files if f.startswith("scraper_") and f.endswith(".py")]

    if not scrapers:
        print(f"❌ No scraper_*.py files found in '{SCRAPER_DIR}'.")
        return

    print(f"Found {len(scrapers)} scrapers:\n")
    for s in scrapers:
        print(f"  - {s}")
    print("\nStarting runs...\n")

    for scraper in scrapers:
        path = os.path.join(SCRAPER_DIR, scraper)
        run_scraper(path)

    print("\n🎉 ALL SCRAPERS FINISHED!")
    print("All JSON files should now be updated.\n")

if __name__ == "__main__":
    main()

