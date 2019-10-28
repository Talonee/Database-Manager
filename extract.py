from bs4 import BeautifulSoup as bs  # webscrape
import requests  # websites
import pandas as pd  # excel sheets
import time


def database():
    with open("Years/citemgr_2002.html", buffering=(2<<16) + 8) as f:
        soup = bs(f.read(), "html.parser")
        cite_id = []
        citation = []
        date = []
        plate = []
        full_name = []
        first = []
        middle = []
        last = []
        status = []

        [
            cite_id.append(i.a.text)
            for i in soup.find_all("td", {"class":"tblkeypcs", "width":"65", "align":"center"})
        ]  # Cite ID

        [
            citation.append(i.text)
            for i in soup.find_all("td", {"align":"center", "width":"80", "class":"tblpcs"})
        ] # Citation

        [
            date.append(i.text)
            for i in soup.find_all("td", {"align":"center", "width":"95", "class":"tblpcs"})
        ] # Date
        
        [
            plate.append(i.text)
            for i in soup.find_all("td", {"align":"center", "width":"85", "class":"tblpcs"})
        ] # Plate

        [
            full_name.append(i.text)
            for i in soup.find_all("td", {"align":"left", "class":"tblpcs"})
        ] # Full name

        # Status
        c = 0
        for i in soup.find_all("td", {"align":"right", "width":"65", "class":"tblpcs"}):
            if c % 2 == 1:
                status.append(i.text)
            c += 1

        for i in full_name:
            if i != "":  # if result is not empty
                name = i.replace(",", " ")
                name = name.split()
                try:  # check for first + middle names
                    f_m = " ".join(name[1:]).split()
                    first.append(f_m[0])
                    try:  # check for multiple middle names
                        middle.append(" ".join(f_m[1:]))
                    except:
                        middle.append(f_m[1])
                    last.append(name[0])
                except:  # only a single word is present
                    first.append(name[0])
                    middle.append("")
                    last.append("")
            else:
                first.append("")
                middle.append("")
                last.append("")

    return cite_id, citation, date, plate, full_name, first, middle, last, status


def web():
    sheet = {}
    sheet["Cite ID"], sheet["Citation"], sheet["Date"], sheet["Plate"], sheet[
        "Full Name"], sheet["First"], sheet["Middle"], sheet["Last"], sheet[
            "Status"] = database()
    sheet["State"] = []
    sheet["Violation"] = []
    sheet["Amount"] = []

    for id in sheet["Cite ID"]:  # State, amount, violation (web)
        url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(id)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        items = soup2.find('input', {'name': 'license_state'}).get('value')
        sheet["State"].append(items)

        num = sheet["Citation"][sheet["Cite ID"].index(id)]
        url = "http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid={}&cite_number={}".format(id, num)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        num = []
        [
            num.append(i.get_text().split()[0][1:])
            if "#" in i.get_text() else "" for i in soup2.find_all(
                "td", align="left", bgcolor="#eeeeee", class_="tblpcs")
        ]
        sheet["Violation"].append("#" + ",".join(num))

        amnt = soup2.find("td", class_="menuheader",
                          bgcolor="#8B6914").get_text()
        amnt_clean = "{}".format(amnt.split()[2])
        sheet["Amount"].append(amnt_clean)
        
    return sheet


def export_excel(table, name):
    df = pd.DataFrame.from_dict(table, orient="index").transpose()
    df = df[[
        "Cite ID", "Citation", "Date", "Plate", "State", "Full Name", "First",
        "Middle", "Last", "Violation", "Amount", "Status"
    ]]
    export_csv = df.to_csv(name, index=False)


if __name__ == "__main__":    
    start = time.time()
    export_excel(web(), "Copy of 2002.csv")
    print("Time: {}".format(time.time()-start))