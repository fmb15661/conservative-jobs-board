from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def get_driver():
    o = Options()
    o.add_argument("--headless=new")
    return webdriver.Chrome(options=o)

url="https://yaf.org/careers/salesforce-administrator/"

d=get_driver()
d.get(url)
time.sleep(2)
soup=BeautifulSoup(d.page_source,"html.parser")
d.quit()

title=soup.select_one("h1").get_text(strip=True)
print("TITLE:", title)

# Now print next 20 text lines after the title
found=False
count=0
for tag in soup.find_all():
    txt=tag.get_text(" ",strip=True)
    if txt==title:
        found=True
        continue
    if found and txt:
        print(txt)
        count+=1
        if count>=20:
            break

