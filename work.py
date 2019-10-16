from bs4 import BeautifulSoup as bs # webscrape
import requests # websites
import codecs # files

# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")

f = codecs.open("citemgr_ex1.html", "r", "utf-8")

soup = bs(f.read(), "html.parser")

print(soup.find("td", class_="tblkeypcs").a.get_text()) # Cite ID
for i in soup.find_all("td", class_="tblpcs"):
    print(i.get_text())



    