from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs  # webscrape html codes
import requests  # requests websites' html codes
import pandas as pd
import time

USERNAMES = []

def login():
    driver = webdriver.Chrome()
    driver.get('https://victorvalley.parkadmin.com/admin/start/login.aro')
    with open("login.txt") as f:
        f = f.read().splitlines()
        un = f[0]
        pw = f[1]

    id_box = driver.find_element_by_id("username")
    id_box.send_keys(un)

    pass_box = driver.find_element_by_id("password")
    pass_box.send_keys(pw)

    login_button = driver.find_element_by_id("login")
    login_button.click()

    return driver


def nav_user_registration(driver):
    driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/a").click()
    driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[2]/a").click()


def new_entry(driver, active, user, account, email, name, address):
    # Active status
    if active:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[3]/td/input").click()

    # User Type
    driver.find_element_by_id("tst_selectUserType").click()
    if user == 1:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[2]").click()
    elif user == 2:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[3]").click()
    elif user == 3:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[4]").click()
    elif user == 4:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[5]").click()
    elif user == 5:
        driver.find_element_by_xpath(
            "/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[6]").click()

    # Username and password
    driver.find_element_by_id("tst_username").send_keys(account[0])
    driver.find_element_by_id("tst_password").clear()
    driver.find_element_by_id("tst_password").send_keys(account[1])

    # Email
    driver.find_element_by_id("tst_emailAddress").send_keys(email)

    # Name
    driver.find_element_by_id("tst_firstName").send_keys(name[0])
    driver.find_element_by_id("tst_middleName").send_keys(name[1])
    driver.find_element_by_id("tst_lastName").send_keys(name[2])

    # Address
    driver.find_element_by_id("tst_localMailingAddress").send_keys(address[0])
    driver.find_element_by_xpath(
        "/html/body/div[1]/form/table[2]/tbody[1]/tr[15]/td/input").send_keys(address[1])
    driver.find_element_by_xpath(
        "/html/body/div[1]/form/table[2]/tbody[1]/tr[16]/td/select").click()
    driver.find_element_by_xpath(
        "/html/body/div[1]/form/table[2]/tbody[1]/tr[16]/td/select").send_keys(address[2])
    driver.find_element_by_id("tst_postalCode").send_keys(address[3])
    driver.find_element_by_id("tst_localPhoneNumber").send_keys(address[4])


def nav_user_search():
    # Navigate to User Search panel
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/a")
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[3]/a")

    # Input specification and limit search data here.
    # Currently empty because this program wants to see all users at once.

    # Proceed to search
    click("/html/body/div[1]/div/form/table/tbody/tr[8]/td/button")

    new_users = []
    names, response = storage_response()
    
    select = Select(driver.find_element_by_name('userstart'))
    page_count = len(select.options)
    page = 1
    while page <= page_count: # current pg# and tote# of options
        select = Select(driver.find_element_by_name('userstart'))
        select.select_by_value("{}".format(page))
        time.sleep(2)
        print(page)
        # View number of users currently presented
        rows_count = driver.execute_script("return document.getElementsByTagName('tr').length") - 9
    
        # Since some users relocate after being edited, 
        # this loop ensures all entries are properly considered
        i = 1
        while i <= 30:
            # Find username at current iteration
            username = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[3]/a".format(i)).text
            if username in names or username + " - invalid address" in names:
                i += 1
            else:
                curr_name = edit_user(i, username, names)
                new_users.append(curr_name)
                names.append(curr_name)
            
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                driver.refresh() # Refresh webpage

        # Reset existing usernames if response is no, else append
        store_users(new_users, True) if response == "n" else store_users(new_users)
        new_users = []
        page += 1
    

def storage_response():
    print("Would you like to read in existing user names? y/n")
    response = "y"
    while response != "y" and response != "n":
        print("Invalid response. Please respond with y/n")
        response = input()

    # Read existing usernames if response is yes, else nothing
    names = read_users() if response == "y" else []

    return names, response

def edit_user(i, username, names): # IN PROGRESS
    df = pd.read_csv("Work files/name-abbr.csv", names=["State", "Abbr"], header=None, index_col=0)

    address = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[5]".format(i)).text
    city = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[6]".format(i)).text

    # Open Mr. Google and search address
    driver.execute_script("window.open('http://www.google.com/');")
    driver.switch_to.window(driver.window_handles[1])
    search = driver.find_element_by_name('q')
    search.send_keys("{} {}".format(address, city))
    search.send_keys(Keys.RETURN)

    # run iff Mr. Google returns a valid address
    try: 
        # Extract and revise address information
        rev_add = driver.find_element_by_class_name("desktop-title-content").text
        rev_csz = driver.find_element_by_class_name("desktop-title-subcontent").text
        city = rev_csz.split(", ")[0]
        state = df.index[df['Abbr'] == (rev_csz.split(", ")[1].split(" ")[0])][0]
        zipcode = rev_csz.split(", ")[1].split(" ")[1]

        # Close search tab and switch back to the original tab
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        # Access and edit user page
        print(username)
        path = "/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[3]/a".format(i)
        user_url = driver.find_element_by_xpath(path).get_attribute("href")
        driver.execute_script("window.open('{}');".format(user_url))
        driver.switch_to.window(driver.window_handles[1])
        click("/html/body/div[1]/div/div[1]/div[1]/div[1]/a")

        # Check for name validity (title case with no trailing spaces)
        name = data_valid("/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[10]/td/input")
        mid = data_valid("/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[11]/td/input")
        last = data_valid("/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[12]/td/input")

        # Enter user data into input fields
        enter_field(name, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[10]/td/input")
        enter_field(mid, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[11]/td/input")
        enter_field(last, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[12]/td/input")
        enter_field(rev_add, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[14]/td/textarea")
        enter_field(city, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[15]/td/input")
        enter_field(state, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[16]/td[2]/select")
        enter_field(zipcode, "/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[17]/td/input")
        time.sleep(2)

        # Submit and confirm changes
        click("/html/body/div[1]/form/table/tbody/tr[2]/td/p/input[1]")
        click("//input[@value='Information Correct']")
    except: # if no valid address found, return usernam as invalid address
        return username + " - invalid address"

    return username

# Store usernames into storage file
def store_users(names, reset=False):
    if reset:
        f = open("storage.txt", "w+")
    else:
        try:
            f = open("storage.txt", "a+")
        except:
            f = open("storage.txt", "w+")
    
    for i in names:
        f.write("{}\n".format(i))
    f.close()

# Read usernames from storage file
def read_users():
    res = []
    try:
        f = open("storage.txt", "r")    
        [res.append(line.strip()) for line in f.readlines()]
    except:
        f = open("storage.txt", "x")    

    return res

# Click an xpath element
def click(path):
    link = driver.find_element_by_xpath(path)
    driver.execute_script("arguments[0].click();", link)
    time.sleep(0.5)

# Clean data (negate empty values, return title case)
def data_valid(path):
    try:
        data = driver.find_element_by_xpath(path).get_attribute("value").strip()
        return data.title() if len(data) > 2 and data != data.title() else data
    except:
        return ""

# Clear input field and insert new data
def enter_field(entry, path):
    field = driver.find_element_by_xpath(path)
    try:
        field.clear()
    except:
        pass
    field.send_keys(entry)


# TODO:
# put all existing username into a list IN SEPERATE TEXT FILE,
# Read that file into a list, THEN decide if you need to edit that user



if __name__ == "__main__":
    driver = login()
    nav_user_search()
    # driver.quit()

    # names = ["zeze", "on goyd", "fraud", "auuuuu", "blew the coug"]
    # store_users(names)
    # dank = read_users()

    # nav_user_registration(driver)
    # new_user(driver, True, 2, ["User", "Password"], "Email", ["Jaden", "Syre", "Smith"],
    #          ["Address", "San Francisco", "Sasketchewan", "00000", "7777777777"])




'''
# class Entry:
    def __init__(self, citeid, citation, date, plate, state, full, first, mid, last, viol, amnt, status, make, model, color):
        self.citeid = citeid
        self.citation = citation
        self.date = date
        self.plate = plate
        self.state = state
        self.full = full
        self.first = first
        self.mid = mid
        self.last = last
        self.viol = viol
        self.amnt = amnt
        self.status = status
        self.make = make
        self.model = model
        self.color = color
        self.dvr = dvr
        self.dvr_addy = dvr_addy
        self.dvr_city = dvr_city
        self.dvr_fone = dvr_fone
        self.own = own
        self.coown = coown
        self.own_addy = own_addy
        self.own_city = own_city
        self.own_fone = own_fone
'''