import sys
import requests
from bs4 import BeautifulSoup

def extract_tm_org_from_soup(soup):
    about = soup.find(string=lambda t: isinstance(t, str) and "about the" in t.lower())
    if not about:
        return None
    parent = about.find_parent()
    if not parent:
        return None
    text = parent.get_text(" ", strip=True)
    for hdr in ["About the Organization:", "About The Organization:", "About the organisation:", "About The Organisation:", "About the Role:", "About The Role:"]:
        if text.startswith(hdr):
            text = text[len(hdr):].strip()
            break
    org = text.split(".")[0].strip()
    return org or None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tm_org_test.py <TalentMarket Job URL>")
        sys.exit(1)

    url = sys.argv[1]
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    org = extract_tm_org_from_soup(soup)
    print(org if org else "NO ORG FOUND")

if __name__ == "__main__":
    main()

