from bs4 import BeautifulSoup as bs
import requests

# page = requests.get("http://citemgr/citemgr/cite_manager.php")

soup = bs("citemgr_ex1.html", features="html.parser")
print(soup.prettify())
