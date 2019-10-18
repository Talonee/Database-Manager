from bs4 import BeautifulSoup as bs  # webscrape
import requests  # websites
import codecs  # files
import pandas as pd  # excel sheets

# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")


def init_excel():
    sheet = {
        "Cite ID": [],
        "Cite Number": [],
        "Date Issued": [],
        "License Number": [],
        "Full Name": [],
        "Status": [],
        "Violation": [],
        "Amount": [],
        "State": [],
        "First": [],
        "Middle": [],
        "Last": []
    }

    return sheet


def export_excel(table, name):
    df = pd.DataFrame.from_dict(table, orient="index").transpose()
    df = df[[
        "Cite ID", "Cite Number", "Date Issued", "License Number", "State",
        "Full Name", "First", "Middle", "Last", "Violation", "Amount", "Status"
    ]]
    export_csv = df.to_csv(name, index=False)


def entry_data_mod():
    f = codecs.open("citemgr_2013_small.html", "r", "utf-8")
    soup = bs(f.read(), "html.parser")

    sheet = init_excel()
    column = 0

    for i in soup.find_all("td", class_="tblkeypcs"):  # Cite ID
        sheet["Cite ID"].append(i.a.get_text())

    for i in soup.find_all(
            "td", class_="tblpcs"):  # Citation, date, license, name, status
        if column == 6:
            column = 0

        if column == 0:
            sheet["Cite Number"].append(i.get_text())
        elif column == 1:
            sheet["Date Issued"].append(i.get_text())
        elif column == 2:
            sheet["License Number"].append(i.get_text())
        elif column == 3:
            sheet["Full Name"].append(i.get_text())
            if i.get_text() != "":  # if result is not empty
                name = i.get_text().replace(",", " ")
                name = name.split()
                try:  # check for first + middle names
                    f_m = " ".join(name[1:]).split()
                    sheet["First"].append(f_m[0])
                    try:  # check for multiple middle names
                        sheet["Middle"].append(" ".join(f_m[1:]))
                    except:
                        sheet["Middle"].append(f_m[1])
                    sheet["Last"].append(name[0])
                except:  # only a single word is present
                    sheet["First"].append(name[0])
                    sheet["Middle"].append("")
                    sheet["Last"].append("")
            else:
                sheet["First"].append("")
                sheet["Middle"].append("")
                sheet["Last"].append("")
        elif column == 4:
            pass
        elif column == 5:
            sheet["Status"].append(i.get_text())

        column += 1

    for i in sheet["Cite ID"]:  # State (web)
        # url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(i)
        # page = requests.get(url)
        # soup2 = bs(page.content, "html.parser")

        f2 = codecs.open("citemgr_ex1_detail.html")
        soup2 = bs(f2.read(), "html.parser")

        state = soup2.find_all("input")
        for i in state:
            if i.get("name") == "license_state":
                sheet["State"].append(i.get("value"))

    for c, value in enumerate(sheet["Cite ID"]):  # Amount, violation (web)
        cite_number = sheet["Cite Number"][c]
        # url = "http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid={}&cite_number={}".format(value, cite_number)
        # page = requests.get(url)
        # soup2 = bs(page.content, "html.parser")

        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        violation = []
        for i in soup2.find_all("td",
                                align="left",
                                bgcolor="#eeeeee",
                                class_="tblpcs"):
            if "#" in i.get_text():
                violation.append(i.get_text().split()[0][1:])
        viol_clean = "#" + ",".join(violation)
        sheet["Violation"].append(viol_clean)

        amount = soup2.find("td", class_="menuheader",
                                bgcolor="#8B6914").get_text()
        amnt_clean = "{}".format(amount.split()[2])
        sheet["Amount"].append(amnt_clean)

    return sheet


if __name__ == "__main__":
    # export_excel(entry_data_mod(), "data_mult.csv")
    print(entry_data_mod())
    # entry_data_mod()
