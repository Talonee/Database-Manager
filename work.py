from bs4 import BeautifulSoup as bs # webscrape
import requests # websites
import codecs # files
import pandas as pd # excel sheets

# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")


def entry_data():
    f = codecs.open("citemgr_ex1.html", "r", "utf-8")

    soup = bs(f.read(), "html.parser")

    data = []
    data.append(soup.find("td", class_="tblkeypcs").a.get_text()) # Cite ID

    for i in soup.find_all("td", class_="tblpcs"):
        data.append(i.get_text())
    
    return data

def init_excel():
    sheet = {
        "Cite ID": [],
        "Cite Number": [],
        "Date Issued": [],
        "License Number": [],
        "Registered Owner": [],
        "Status": []
        }
    
    return sheet

def excel_input():
    sheet = init_excel()
    data = entry_data()

    sheet["Cite ID"].append(data[0])
    sheet["Cite Number"].append(data[1])
    sheet["Date Issued"].append(data[2])
    sheet["License Number"].append(data[3])
    sheet["Registered Owner"].append(data[4])
    sheet["Status"].append(data[6])

    return sheet

def export_excel():
    df = pd.DataFrame(excel_input())
    export_csv = df.to_csv("data.csv", index=False)

    

if __name__ == "__main__":
    export_excel()
    