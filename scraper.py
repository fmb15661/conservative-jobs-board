import pandas as pd
import json
from datetime import datetime

excel_path = "Job boards list.xlsx"
df = pd.read_excel(excel_path, sheet_name="Sheet 1")

df.columns = df.iloc[0]
df = df[1:]
df = df.rename(columns={
    "Employer": "organization",
    "Careers Page": "career_page",
    "Home Page": "home_page"
})

jobs_data = []
for _, row in df.iterrows():
    org = row.get("organization")
    career_page = row.get("career_page")
    if pd.isna(career_page) or career_page == "":
        continue
    jobs_data.append({
        "organization": org,
        "career_page": career_page,
        "jobs": [{"title": "See listings", "link": career_page}],
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

with open("jobs.json", "w") as f:
    json.dump(jobs_data, f, indent=2)

print(f"✅ {len(jobs_data)} organizations saved to jobs.json")
