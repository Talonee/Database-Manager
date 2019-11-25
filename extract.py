from bs4 import BeautifulSoup as bs  # webscrape html codes
import requests  # requests websites' html codes
import pandas as pd  # dataframes and export
import time # measure run speed
import datetime # support time
from encode import encode as ec
from decode import decode as dc

# Retrieve data for cite ID, citation number, date, plate, full name, and status
def database():
    with open("Years/citemgr_1999.html", buffering=(2 << 16) + 8) as f:
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
            for i in soup.find_all("td", {"class": "tblkeypcs", "width": "65", "align": "center"})
        ]  # Cite ID

        [
            citation.append(i.text)
            for i in soup.find_all("td", {"align": "center", "width": "80", "class": "tblpcs"})
        ]  # Citation

        [
            date.append(i.text)
            for i in soup.find_all("td", {"align": "center", "width": "95", "class": "tblpcs"})
        ]  # Date

        [
            plate.append(i.text)
            for i in soup.find_all("td", {"align": "center", "width": "85", "class": "tblpcs"})
        ]  # Plate

        [
            full_name.append(i.text)
            for i in soup.find_all("td", {"align": "left", "class": "tblpcs"})
        ]  # Full name

        # Status
        c = 0
        for i in soup.find_all("td", {"align": "right", "width": "65", "class": "tblpcs"}):
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

# Retrieve data for state, amount, and violation.
def web():
    sheet = {}
    sheet["Cite ID"], sheet["Citation"], sheet["Date"], sheet["Plate"], sheet[
        "Full Name"], sheet["First"], sheet["Middle"], sheet["Last"], sheet["Status"] = database()
    sheet["State"] = []
    sheet["Violation"] = []
    sheet["Amount"] = []

    for id in sheet["Cite ID"]: 
        url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(
            id)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        items = soup2.find('input', {'name': 'license_state'}).get('value')
        sheet["State"].append(items)

        num = sheet["Citation"][sheet["Cite ID"].index(id)]
        url = "http://citemgr/citemgr/violation_trans_main.php?cite_array=&cite_sysid={}&cite_number={}".format(
            id, num)
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

# Retrieve data for vehicle description
def vehicle_desc():
    df = pd.read_csv("Output/Copy of 1999.csv")
    make = []
    model = []
    color = []

    for i in df["Cite ID"]:
        url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(
            i)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        make.append(soup2.find('input', {'name': 'vehicle_make'}).get('value'))
        model.append(soup2.find(
            'input', {'name': 'vehicle_model'}).get('value'))
        color.append(soup2.find(
            'input', {'name': 'vehicle_color'}).get('value'))

    df["Vehicle Make"] = make
    df["Vehicle Model"] = model
    df["Vehicle Color"] = color

    return df

# Retrieve data for driver and owner address
def address():
    df = pd.read_csv("Output v2/Copy of 1999 DATA.csv")
    dvr = []
    dvr_addy = []
    dvr_city = []
    dvr_fone = []
    own = []
    coown = []
    own_addy = []
    own_city = []
    own_fone = []

    for i in df["Cite ID"]:
        url = "http://citemgr/citemgr/cite_edit.php?cite_sysid={}&username=".format(i)
        page = requests.get(url)
        soup2 = bs(page.content, "html.parser")

        dvr.append(soup2.find('input', {'name': 'driver_name'}).get('value'))
        dvr_addy.append(soup2.find(
            'input', {'name': 'driver_addr'}).get('value'))
        dvr_city.append(soup2.find(
            'input', {'name': 'driver_csz'}).get('value'))
        dvr_fone.append(soup2.find(
            'input', {'name': 'driver_phone'}).get('value'))
        own.append(soup2.find('input', {'name': 'owner_name'}).get('value'))
        coown.append(soup2.find('input', {'name': 'owner_name2'}).get('value'))
        own_addy.append(soup2.find(
            'input', {'name': 'owner_addr'}).get('value'))
        own_city.append(soup2.find(
            'input', {'name': 'owner_csz'}).get('value'))
        own_fone.append(soup2.find(
            'input', {'name': 'owner_phone'}).get('value'))

    df["Driver Name"] = dvr
    df["Driver Address"] = dvr_addy
    df["Driver CSZ"] = dvr_city
    df["Driver Phone"] = dvr_fone
    df["Owner Name"] = own
    df["Co-Owner"] = coown
    df["Owner Address"] = own_addy
    df["Owner CSZ"] = own_city
    df["Owner Phone"] = own_fone

    return df

# Export data into CSV files
def export_excel(table, name):
    if isinstance(table, pd.DataFrame):
        df = table
    else:
        df = pd.DataFrame.from_dict(table, orient="index").transpose()

    df = df[[
        'Cite ID', 'Citation', 'Date', 'Plate', 'State', 'Full Name', 'First',
       'Middle', 'Last', 'Violation', 'Amount', 'Status', 'Vehicle Make',
       'Vehicle Model', 'Vehicle Color', 'Driver Name', 'Driver Address',
       'Driver CSZ', 'Driver Phone', 'Owner Name', 'Co-Owner', 'Owner Address',
       'Owner CSZ', 'Owner Phone'
    ]]
    export_csv = df.to_csv(name, index=False)

# Clean data of VOID values and blank entries
def clean():
    for i in range(14):
        yr = "0{}".format(i) if i < 10 else i
        input = "Output v3/Copy of 20{} DATA.csv".format(yr)
        output = "Output v4/Copy of 20{} DATA.csv".format(yr)

        csv = pd.read_csv(input)
        i = 0
        while i < csv.shape[0]:
            if pd.isna(csv["Full Name"].iloc[i]) or str(csv["Full Name"].iloc[i]).upper() == "VOID" or str(csv["Status"].iloc[i]).upper() == "VOID" or pd.isna(csv["Plate"].iloc[i]) or str(csv["Plate"].iloc[i]).upper() == "VOID": 
                csv.drop([i], axis=0, inplace = True)
                csv.reset_index(drop = True, inplace = True)    
            else:
                i = i + 1

        export_excel(csv, output)

def anon():
    input = "Output/Copy of 20{} DATA.csv".format(13)
    csv = pd.read_csv(input)
    print(csv["Full Name"].head())
    csv["Full Name"] = list(map(ec, csv["Full Name"]))
    print("\n\n\n")
    print(csv["Full Name"].head())
    print("\n\n---------------------------\n")
    csv["Full Name"] = list(map(dc, csv["Full Name"]))
    print(csv["Full Name"].head())

if __name__ == "__main__":
    # start = time.time()
    # clean()
    # sec = time.time()-start
    # print("Time: {}".format(str(datetime.timedelta(seconds=sec))))
    anon()
