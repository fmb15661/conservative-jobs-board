import json

tm = json.load(open("frontend/public/jobs_talentmarket.json"))
yaf = json.load(open("frontend/public/jobs_yaf.json"))

titles = {j["title"] for j in tm}
final = tm + [j for j in yaf if j["title"] not in titles]

json.dump(final, open("frontend/public/jobs.json","w"), indent=2)
print("done", len(final))
import json

TM = "frontend/public/jobs_talentmarket.json"
YAF = "frontend/public/jobs_yaf.json"
OUT = "frontend/public/jobs.json"

def read_file(path):
    try:
        with open(path) as f:
            return json.load(f)
    except:
        return []

tm = read_file(TM)
yaf = read_file(YAF)

combined = tm + yaf

# DE-DUPE BY LINK
seen = set()
unique = []
for job in combined:
    if job["link"] not in seen:
        unique.append(job)
        seen.add(job["link"])

with open(OUT, "w") as f:
    json.dump(unique, f, indent=2)

print("✅ merged", len(tm), "TM +", len(yaf), "YAF")
print("✅ unique total =", len(unique), "→", OUT)

