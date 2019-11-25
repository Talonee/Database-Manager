from selenium import webdriver
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


def new_user(driver, active, user, account, email, name, address):
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
    # Navigate to user_search
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/a")
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[3]/a")

    # Enter specification into input fields and limit search data here.
    # Default is empty because we want to see all users at once.

    # Proceed to search
    click("/html/body/div[1]/div/form/table/tbody/tr[8]/td/button")

    # View number of users currently presented
    rows_count = driver.execute_script("return document.getElementsByTagName('tr').length") - 8
    
    # Since some users relocate after being edited, 
    # this loop ensures all entries are properly considered
    i = 1
    # while i <= rows_count:
    while i <= 5:
        # Edit user at current iteration and retrieve username
        curr_name = curr_user(i) 
        driver.refresh() # Refresh webpage

        # Extract username at same iteration
        curr_iter = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[3]/a".format(i)).text
        
        # If both usernames match, user did not relocate, new iteration
        if curr_name == curr_iter:
            i += 1
        
        print(curr_name, curr_iter)
        # Else if usernames do not match, rerun same iteration

# UNKNOWN ERROR TO BE SOLVED, NAMES DO NOT UPDATE UPON THIRD ITERATION


def curr_user(i): # IN PROGRESS
    username = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[3]/a".format(i)).text
    
    if username not in USERNAMES: # Check if user is already edited
        df = pd.read_csv("Work files/name-abbr.csv", names=["State", "Abbr"], header=None, index_col=0)
        USERNAMES.append(username)

        address = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[5]".format(i)).text
        city = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[6]".format(i)).text

        # Open and switch to a new search tab
        driver.execute_script("window.open('http://www.google.com/');")
        driver.switch_to.window(driver.window_handles[1])
        search = driver.find_element_by_name('q')
        search.send_keys("{} {}".format(address, city))
        search.send_keys(Keys.RETURN)

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
        submit = driver.find_element_by_xpath("/html/body/div[1]/form/table/tbody/tr[2]/td/p/input[1]")
        driver.execute_script("arguments[0].click();", submit)
        time.sleep(2)
        confirm = driver.find_element_by_xpath("/html/body/div[1]/table/tbody/tr[3]/td/form/input[43]")
        driver.execute_script("arguments[0].click();", confirm)
        time.sleep(2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

    return username

# Click the given xpath element
def click(path):
    link = driver.find_element_by_xpath(path)
    driver.execute_script("arguments[0].click();", link)
    time.sleep(0.5)

# Checks for data validity (title case with no trailing spaces)
def data_valid(path):
    try:
        data = driver.find_element_by_xpath(path).get_attribute("value").strip()
        return data.title() if len(data) > 2 and data != data.title() else data
    except:
        return ""

# Clear pre-existing input fields and insert new data
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

# Try except the google address, if not found, quit asap


if __name__ == "__main__":
    driver = login()
    nav_user_search()
    driver.close()


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