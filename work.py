from bs4 import BeautifulSoup as bs
import requests

page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")

soup = bs(page.content, features="html.parser")
print(soup.prettify())
