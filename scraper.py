#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Conservative Jobs Board Scraper (stable)
- Detects spreadsheet headers and columns automatically
- Platform detection: iCIMS, BambooHR, Workday (generic), + AIER custom
- Robust network handling, timeouts, retries, error isolation
- Never crashes: per-org try/except; fallbacks ensure a row is emitted
- Output: jobs.json sorted newest-first (YYYY-MM-DD)
"""

import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from bs4 import BeautifulSoup

# --- Quiet noisy warnings on some macOS Pythons (LibreSSL vs OpenSSL)
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X) ConservativeJobsBoardBot/1.0 (+contact: site owner)"
TIMEOUT = 25

session = requests.Session()
session.headers.update({"User-Agent": UA})
# Robust retry policy
retries = Retry(
    total=3,
    backoff_factor=0.7,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"]
)
adapter = HTTPAdapter(max_retries=retries, pool_connections=20, pool_maxsize=20)
session.mount("http://", adapter)
session.mount("https://", adapter)

def log(msg: str):
    print(msg, flush=True)

def safe_get(url: str, **kwargs) -> Optional[requests.Response]:
    try:
        r = session.get(url, timeout=TIMEOUT, verify=False, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        log(f"❌ GET failed: {url} -> {e}")
        return None

def safe_post(url: str, **kwargs) -> Optional[requests.Response]:
    try:
        r = session.post(url, timeout=TIMEOUT, verify=False, **kwargs)
        r.raise_for_status()
        return r
    except Exception as e:
        log(f"❌ POST failed: {url} -> {e}")
        return None

def norm_date(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = str(s).strip()
    # prefer ISO or parse obvious formats; keep very defensive
    try:
        # Workday often yields ISO; others vary
        dt = pd.to_datetime(s, errors="coerce", utc=True)
        if pd.isna(dt):
            return None
        return dt.tz_convert(None).strftime("%Y-%m-%d") if hasattr(dt, "tz_convert") else dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def today_iso() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")

# ---------------- Platform detection ----------------

def detect_platform(url: str) -> str:
    u = url.lower()
    if "icims.com" in u:
        return "iCIMS"
    if "bamboohr.com" in u:
        return "BambooHR"
    if any(k in u for k in ["myworkdayjobs.com", "workday", "wd5", "wd1", "wd3"]) or "careers.nfib.com" in u:
        return "Workday"
    # Custom: handle specific sites
    if "aier.org/careers" in u:
        return "AIER_Custom"
    return "Custom"

# ---------------- iCIMS ----------------
def scrape_icims(org: str, career_url: str) -> List[Dict]:
    res = []
    r = safe_get(career_url)
    if not r:
        return res
    soup = BeautifulSoup(r.text, "html.parser")

    # Newer iCIMS implementations can use cards/listings with various classes
    cards = soup.select("div.iCIMS_JobListing, div.row, li[class*='job'], div[class*='search-result']")
    if not cards:
        # fallback: any anchor under the listing container
        cards = soup.select("a.iCIMS_Anchor, .iCIMS_Listings a, .search-results a")

    for c in cards:
        # Try to find anchor
        a = c if c.name == "a" else c.find("a", href=True)
        if not a:
            continue
        title = a.get_text(strip=True) or "Untitled"
        link = a["href"]
        if link.startswith("/"):
            # Build absolute from base
            from urllib.parse import urljoin
            link = urljoin(career_url, link)

        # Try to find location/type in siblings/text
        txt = c.get_text(" ", strip=True)
        # naive extraction
        loc_match = re.search(r"Location[:\s]+(.+?)(?:\s{2,}|$)", txt, flags=re.I)
        jobtype_match = re.search(r"(Full[-\s]?time|Part[-\s]?time|Internship|Fellowship|Contract)", txt, flags=re.I)
        loc = loc_match.group(1).strip() if loc_match else "N/A"
        job_type = jobtype_match.group(1).strip().title() if jobtype_match else "N/A"

        res.append({
            "title": title,
            "organization": org,
            "location": loc,
            "type": job_type,
            "date_posted": today_iso(),   # iCIMS list pages often omit dates; detailed pages may include them
            "link": link
        })
    return res

# ---------------- BambooHR ----------------
# JSON list: https://{sub}.bamboohr.com/careers/list?format=json
def bamboo_subdomain(u: str) -> Optional[str]:
    m = re.search(r"https?://([a-z0-9\-_.]+)\.bamboohr\.com", u.lower())
    return m.group(1) if m else None

def scrape_bamboohr(org: str, career_url: str) -> List[Dict]:
    res = []
    sub = bamboo_subdomain(career_url)
    if not sub:
        return res
    api = f"https://{sub}.bamboohr.com/careers/list?format=json"
    r = safe_get(api)
    if not r:
        return res
    try:
        data = r.json()
    except Exception:
        return res
    for j in data.get("result", []):
        res.append({
            "title": (j.get("jobOpeningName") or "Untitled").strip(),
            "organization": org,
            "location": (j.get("location") or "N/A").strip(),
            "type": (j.get("jobOpeningType") or "N/A").strip(),
            "date_posted": norm_date(j.get("publishedDate")) or today_iso(),
            "link": j.get("jobOpeningUrl") or career_url
        })
    return res

# ---------------- Workday (generic) ----------------
"""
Approach:
1) If URL already on myworkdayjobs.com, attempt /wday/cxs/{tenant}/{site}/jobs search API.
2) If not, fetch HTML and search for an embedded myworkdayjobs.com link; use that as base.
3) POST payload: {"limit":50,"offset":0,"searchText":""}
We gather title, jobPostingInfo -> locations / externalPath.
"""

def find_myworkday_base(html: str) -> Optional[str]:
    # Look for any https://*.myworkdayjobs.com/{tenant}/{site}
    m = re.search(r"https://[a-z0-9\-.]+\.myworkdayjobs\.com/[^\"'\s<>]+", html, re.I)
    return m.group(0) if m else None

def build_cxs_endpoint(base: str) -> Optional[str]:
    # Convert ...myworkdayjobs.com/{tenant}/{site}/... -> .../wday/cxs/{tenant}/{site}/jobs
    try:
        parts = base.split("myworkdayjobs.com/")[1].split("/")
        # Expect e.g. tenant/site
        if len(parts) < 2:
            return None
        tenant = parts[0]
        site = parts[1]
        return f"https://{base.split('://',1)[1].split('/')[0]}/wday/cxs/{tenant}/{site}/jobs"
    except Exception:
        return None

def scrape_workday(org: str, career_url: str) -> List[Dict]:
    res = []
    # Step 1: get a myworkday base
    base = None
    if "myworkdayjobs.com" in career_url:
        base = career_url
    else:
        r0 = safe_get(career_url)
        if r0 and r0.text:
            base = find_myworkday_base(r0.text)
    if not base:
        return res

    cxs = build_cxs_endpoint(base)
    if not cxs:
        return res

    payload = {"limit": 50, "offset": 0, "searchText": ""}

    r = safe_post(cxs, json=payload, headers={"Content-Type": "application/json"})
    if not r:
        return res
    try:
        data = r.json()
    except Exception:
        return res

    for item in data.get("jobPostings", []):
        title = (item.get("title") or "Untitled").strip()
        # Construct external link if present
        # externalPath is often present; base up to domain + tenant/site:
        external_path = item.get("externalPath") or item.get("externalUrl") or ""
        link = None
        if external_path:
            # base like https://<domain>.myworkdayjobs.com/{tenant}/{site}/job/<externalPath>
            try:
                dom = cxs.split("/wday/cxs/")[0]
                tenant_site = cxs.split("/wday/cxs/")[1].split("/jobs")[0]
                link = f"{dom}/{tenant_site}/job/{external_path}"
            except Exception:
                link = None
        link = link or career_url

        # locations: array of strings or dicts varies by tenant
        loc = "N/A"
        if "locations" in item and isinstance(item["locations"], list) and item["locations"]:
            loc = ", ".join([str(x) for x in item["locations"] if x])

        # datePosted: often ISO
        date_posted = norm_date(item.get("postedOn")) or norm_date(item.get("startDate")) or today_iso()

        # type/commitment not standardized; leave N/A
        res.append({
            "title": title,
            "organization": org,
            "location": (loc or "N/A"),
            "type": "N/A",
            "date_posted": date_posted,
            "link": link
        })

    return res

# ---------------- AIER (custom) ----------------
def scrape_aier(org: str, career_url: str) -> List[Dict]:
    """
    AIER WordPress careers page: extract obvious job listing anchors under content.
    We’ll pull <article> or main content links that look like postings.
    """
    res = []
    r = safe_get(career_url)
    if not r:
        return res
    soup = BeautifulSoup(r.text, "html.parser")

    # Heuristics: list items, content blocks under main with anchor text that isn't just 'Apply'
    anchors = soup.select("main a, article a, .entry-content a")
    seen = set()
    for a in anchors:
        href = a.get("href")
        text = (a.get_text(strip=True) or "")
        if not href or not text:
            continue
        # Ignore obvious nav or unrelated links
        if len(text) < 4:
            continue
        if re.search(r"(apply|donate|contact|privacy|terms)", text, re.I):
            continue
        # Heuristic: if the link is on aier.org and looks like a post/page, consider it a job entry
        if "aier.org" in href:
            key = (text, href)
            if key in seen:
                continue
            seen.add(key)
            res.append({
                "title": text,
                "organization": org,
                "location": "N/A",
                "type": "N/A",
                "date_posted": today_iso(),
                "link": href
            })

    # If nothing matched, fallback
    if not res:
        res.append({
            "title": "View Jobs",
            "organization": org,
            "location": "N/A",
            "type": "N/A",
            "date_posted": today_iso(),
            "link": career_url
        })
    return res

# ---------------- Fallback ----------------
def fallback_entry(org: str, url: str) -> List[Dict]:
    return [{
        "title": "View Jobs",
        "organization": org,
        "location": "N/A",
        "type": "N/A",
        "date_posted": today_iso(),
        "link": url
    }]

# ---------------- Dispatch ----------------
def scrape_for_org(org: str, url: str) -> List[Dict]:
    platform = detect_platform(url)
    log(f"🔎 {org}: {platform}")
    try:
        if platform == "iCIMS":
            out = scrape_icims(org, url)
        elif platform == "BambooHR":
            out = scrape_bamboohr(org, url)
        elif platform == "Workday":
            out = scrape_workday(org, url)
        elif platform == "AIER_Custom":
            out = scrape_aier(org, url)
        else:
            out = fallback_entry(org, url)
    except Exception as e:
        log(f"❌ Scrape error for {org} ({platform}): {e}")
        out = fallback_entry(org, url)

    # Normalize & harden
    cleaned = []
    for j in out:
        cleaned.append({
            "title": str(j.get("title") or "View Jobs"),
            "organization": str(j.get("organization") or org),
            "location": str(j.get("location") or "N/A"),
            "type": str(j.get("type") or "N/A"),
            "date_posted": norm_date(j.get("date_posted")) or today_iso(),
            "link": str(j.get("link") or url)
        })
    return cleaned

# ---------------- Excel ingestion ----------------
def load_orgs_from_excel(path: str) -> List[Dict]:
    """
    Returns list of dicts: [{"org": "...", "url": "..."}, ...]
    Auto-detects header row and the org/url columns (employer|organization|company / career|job|url|link).
    """
    # Read with no header; some Numbers exports include metadata rows
    df = pd.read_excel(path, sheet_name=0, header=None)
    # Find header row
    header_row_idx = None
    for i, row in df.iterrows():
        row_str = " ".join(str(x).lower() for x in row if pd.notna(x))
        if any(k in row_str for k in ["employer", "organization", "company", "org"]) and \
           any(k in row_str for k in ["career", "job", "url", "link"]):
            header_row_idx = i
            break
    if header_row_idx is None:
        # fallback: try skipping first 10 rows and assume row 0 as header
        df = pd.read_excel(path, sheet_name=0, header=None, skiprows=10)
        if not df.empty:
            header_row_idx = 0
        else:
            raise ValueError("Could not detect header row in spreadsheet.")

    # Apply header and trim
    df = pd.read_excel(path, sheet_name=0, header=None)  # reload raw
    df.columns = df.iloc[header_row_idx]
    df = df.drop(list(range(0, header_row_idx + 1))).dropna(how="all")

    # Detect columns
    norm = {c: str(c).strip().lower() for c in df.columns}
    org_col = next((col for col, n in norm.items() if any(k in n for k in ["employer", "organization", "company", "org"])), None)
    url_col = next((col for col, n in norm.items() if any(k in n for k in ["career", "job", "url", "link"])), None)
    if not org_col or not url_col:
        raise ValueError(f"Could not find org/URL columns. Found: {list(df.columns)}")

    # Pull rows
    df = df.dropna(subset=[org_col, url_col], how="any")
    pairs = []
    for _, row in df.iterrows():
        org = str(row[org_col]).strip()
        url = str(row[url_col]).strip()
        if not org or not url or url.lower() == "nan":
            continue
        pairs.append({"org": org, "url": url})
    return pairs

# ---------------- Main ----------------
def main():
    excel_path = "Job boards list.xlsx"  # keep exact name used earlier

    try:
        orgs = load_orgs_from_excel(excel_path)
    except Exception as e:
        log(f"❌ Spreadsheet problem: {e}")
        log("Tip: Open your spreadsheet, delete the metadata rows above the actual headers, and re-save.")
        return

    log(f"📄 Loaded {len(orgs)} orgs from spreadsheet")

    all_jobs: List[Dict] = []
    seen = set()

    for idx, item in enumerate(orgs, 1):
        org, url = item["org"], item["url"]
        log(f"[{idx}/{len(orgs)}] {org} -> {url}")
        jobs = scrape_for_org(org, url)

        for j in jobs:
            key = (j["title"], j["link"])
            if key in seen:
                continue
            seen.add(key)
            all_jobs.append(j)

        # politeness delay
        time.sleep(0.5)

    # Sort newest-first
    def sort_key(j):
        try:
            return datetime.strptime(j.get("date_posted", ""), "%Y-%m-%d")
        except Exception:
            return datetime(1970, 1, 1)

    all_jobs.sort(key=sort_key, reverse=True)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2, ensure_ascii=False)

    # Summary
    log("—" * 60)
    log(f"✅ Saved {len(all_jobs)} jobs to jobs.json")
    by_org = {}
    for j in all_jobs:
        by_org.setdefault(j["organization"], 0)
        by_org[j["organization"]] += 1
    top = sorted(by_org.items(), key=lambda x: x[1], reverse=True)[:10]
    log("Top orgs by jobs:")
    for org, n in top:
        log(f"  • {org}: {n}")

if __name__ == "__main__":
    main()
