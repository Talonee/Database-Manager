from bs4 import BeautifulSoup as bs  # webscrape
import requests  # websites
import codecs  # files
import pandas as pd  # excel sheets

# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")


def export_excel(table, name):
    df = pd.DataFrame.from_dict(table, orient="index").transpose()
    df = df[[
        "Cite ID", "Citation", "Date", "Plate", "State", "Full Name", "First",
        "Middle", "Last", "Violation", "Amount", "Status"
    ]]
    export_csv = df.to_csv(name, index=False)


def database():
    f = codecs.open("citemgr_2013.html", "r", "utf-8")
    soup = bs(f.read(), "html.parser")
    column = 0
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
        cite_id.append(i.a.get_text())
        for i in soup.find_all("td", class_="tblkeypcs")
    ]  # Cite ID

    for i in soup.find_all(
            "td", class_="tblpcs"):  # Citation, date, plate, name*3, status
        if column == 6:
            column = 0

        if column == 0:
            citation.append(i.get_text())
        elif column == 1:
            date.append(i.get_text())
        elif column == 2:
            plate.append(i.get_text())
        elif column == 3:
            full_name.append(i.get_text())
            if i.get_text() != "":  # if result is not empty
                name = i.get_text().replace(",", " ")
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
        elif column == 4:
            pass
        elif column == 5:
            status.append(i.get_text())

        column += 1

    f.close()

    return cite_id, citation, date, plate, full_name, first, middle, last, status


def web():
    sheet = sheet1()
    state = []
    violation = []
    amount = []

    for i in sheet["Cite ID"]:  # State (web)
        # url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(i)
        # page = requests.get(url)
        # soup2 = bs(page.content, "html.parser")

        f2 = codecs.open("citemgr_ex1_detail.html")
        soup2 = bs(f2.read(), "html.parser")

        items = soup2.find_all("input")
        for i in items:
            if i.get("name") == "license_state":
                state.append(i.get("value"))

    for id in sheet["Cite ID"]:  # Amount, violation (web)
        # num = sheet["Cite Number"][sheet["Cite ID"].index(id)]
        # url = "http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid={}&cite_number={}".format(id, num)
        # page = requests.get(url)
        # soup2 = bs(page.content, "html.parser")

        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        num = []
        [
            num.append(i.get_text().split()[0][1:])
            if "#" in i.get_text() else "" for i in soup2.find_all(
                "td", align="left", bgcolor="#eeeeee", class_="tblpcs")
        ]
        violation.append("#" + ",".join(num))

        amnt = soup2.find("td", class_="menuheader",
                          bgcolor="#8B6914").get_text()
        amnt_clean = "{}".format(amnt.split()[2])
        amount.append(amnt_clean)

    return state, violation, amount


def sheet1():
    sheet = {}
    sheet["Cite ID"], sheet["Citation"], sheet["Date"], sheet["Plate"], sheet[
        "Full Name"], sheet["First"], sheet["Middle"], sheet["Last"], sheet[
            "Status"] = database()
    return sheet


def sheet2():
    sheet = {}
    sheet["State"], sheet["Violation"], sheet["Amount"] = web()
    return sheet


if __name__ == "__main__":

    # export_excel(database(), "test.csv")
    # export_excel({**sheet1(), **sheet2()}, "data_mult.csv")
    export_excel(sheet1(), "data_sheet1.csv")
    # export_excel(sheet2(), "data_sheet2.csv")
