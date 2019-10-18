from bs4 import BeautifulSoup as bs  # webscrape
import requests  # websites
import codecs  # files
import pandas as pd  # excel sheets

import time
# request website
# page = requests.get("http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid=83813&cite_number=1306-25673")

# make database and web return all columns then create a single fxn to put in sheet at once
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


def export_excel(table, name):
    df = pd.DataFrame.from_dict(table, orient="index").transpose()
    df = df[[
        "Cite ID", "Cite Number", "Date Issued", "License Number", "State",
        "Full Name", "First", "Middle", "Last", "Violation", "Amount", "Status"
    ]]
    export_csv = df.to_csv(name, index=False)


def database():
    f = codecs.open("citemgr_2013.html", "r", "utf-8")
    soup = bs(f.read(), "html.parser")
    column = 0

    [sheet["Cite ID"].append(i.a.get_text()) for i in soup.find_all("td", class_="tblkeypcs")] # Cite ID

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

    return sheet

def web():
    sheet = init_excel()

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

    for id in sheet["Cite ID"]:  # Amount, violation (web)
        # num = sheet["Cite Number"][sheet["Cite ID"].index(id)]
        # url = "http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid={}&cite_number={}".format(id, num)
        # page = requests.get(url)
        # soup2 = bs(page.content, "html.parser")

        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        violation = []
        # for i in soup2.find_all("td",
        #                         align="left",
        #                         bgcolor="#eeeeee",
        #                         class_="tblpcs"):
        #     if "#" in i.get_text():
        #         violation.append(i.get_text().split()[0][1:])
        # viol_clean = "#" + ",".join(violation)
        # sheet["Violation"].append(viol_clean)

    
        [violation.append(i.get_text().split()[0][1:]) if "#" in i.get_text() else "" for i in soup2.find_all("td",
                                align="left",
                                bgcolor="#eeeeee",
                                class_="tblpcs")]
        sheet["Violation"].append("#" + ",".join(violation))

        # fx = (lambda x: x.get_text().split()[0][1:] if "#" in x.get_text() else None)
        # violation = list(map(fx, soup2.find_all("td",
        #                         align="left",
        #                         bgcolor="#eeeeee",
        #                         class_="tblpcs")))
        # violation = [i for i in violation if i]
        # sheet["Violation"].append("#" + ",".join(violation))


        amount = soup2.find("td", class_="menuheader",
                                bgcolor="#8B6914").get_text()
        amnt_clean = "{}".format(amount.split()[2])
        sheet["Amount"].append(amnt_clean)

    return sheet


def mod1(): # for loop

    for id in sheet["Cite ID"]:  # Amount, violation (web)
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

def mod2(): # List comprehension

    for id in sheet["Cite ID"]:  # Amount, violation (web)
        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        violation = []
        [violation.append(i.get_text().split()[0][1:]) if "#" in i.get_text() else "" for i in soup2.find_all("td",
                                align="left",
                                bgcolor="#eeeeee",
                                class_="tblpcs")]
        sheet["Violation"].append("#" + ",".join(violation))

def mod3(): # Lambda map

    for id in sheet["Cite ID"]:  # Amount, violation (web)
        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        fx = (lambda x: x.get_text().split()[0][1:] if "#" in x.get_text() else None)
        violation = list(map(fx, soup2.find_all("td",
                                align="left",
                                bgcolor="#eeeeee",
                                class_="tblpcs")))
        violation = [i for i in violation if i]
        sheet["Violation"].append("#" + ",".join(violation))

def mod4_init(): # generator    
    for id in sheet["Cite ID"]:
        f2 = codecs.open("citemgr_ex1_mult_trans.html", "r", "utf-8")
        soup2 = bs(f2.read(), "html.parser")

        for i in soup2.find_all("td",
                                align="left",
                                bgcolor="#eeeeee",
                                class_="tblpcs"):
            if "#" in i.get_text():
                yield i.get_text().split()[0][1:]

def mod4():
    violation = []
    [violation.append(i) for i in mod4_init()]
    sheet["Violation"].append("#" + ",".join(violation))


if __name__ == "__main__":
    # export_excel(entry_data_mod(), "data_mult.csv")
    # export_excel(entry_data_mod2(), "data_test.csv")

    # export_excel(database(), "test.csv")
    database()

    start = time.time()
    mod1()
    print("For-loop: {}".format(time.time() - start))

    start = time.time()
    mod2()
    print("List Comp: {}".format(time.time() - start))

    start = time.time()
    mod3()
    print("LambdaMap: {}".format(time.time() - start))

    start = time.time()
    mod4()
    print("Generator: {}".format(time.time() - start))

    # print(entry_data_mod())
    # entry_data_mod()

    # result = []
    # dank = ["#  ", "yuh#", "0", "abc"]
    # fx = (lambda x: x if "#" in x else "")
    # result = list(map(fx, dank))
    # print(result)

    # result = []
    # dank = ["#  ", "yuh#", "0", "abc"]
    # [result.append(x) if "#" in x else "" for x in dank]
    # print(result)
