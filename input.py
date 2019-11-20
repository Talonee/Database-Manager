from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs  # webscrape html codes
import requests  # requests websites' html codes
import pandas as pd
import time


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


def nav_user_search(driver):
    # navigate to user_search
    driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/a").click()
    driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[3]/a").click()

    # code for field inputs here

    # proceed to search
    btn = driver.find_element_by_xpath("/html/body/div[1]/div/form/table/tbody/tr[8]/td/button")
    btn.click()

    # current_name(driver.current_url) # TODO
    current_list(driver.current_url)

def current_list(url): # IN PROGRESS
    address = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[1]/td[5]").text
    city = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[1]/td[6]").text

    driver.execute_script("window.open('http://www.google.com/');") # open search tab
    driver.switch_to.window(driver.window_handles[1]) # switch to search tab
    search = driver.find_element_by_name('q')
    search.send_keys("{} {}".format(address, city))
    search.send_keys(Keys.RETURN)

    rev_add = driver.find_element_by_class_name("desktop-title-content").text
    rev_csz = driver.find_element_by_class_name("desktop-title-subcontent").text

    driver.close()
    driver.switch_to.window(driver.window_handles[0]) # switch back to first tab

    user = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[1]/td[3]/a")
    user.click()    

    edit = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[1]/div[1]/a")
    edit.click()

    mail_address = driver.find_element_by_xpath("/html/body/div[1]/form/table/tbody/tr[2]/td/table/tbody[1]/tr[14]/td/textarea")
    mail_address.clear()
    mail_address.send_keys(rev_add)

    city = rev_csz.split(",")[0]
    state = rev_csz.split(",")[0].split(" ")[0]
    zipcode = rev_csz.split(",")[0].split(" ")[1]



    print(rev_add, rev_csz)

if __name__ == "__main__":
    # driver = login()

    # nav_user_search(driver)
    # driver.close()

    df = pd.read_csv("name-abbr.csv", names=["State", "Abbr"], header=None)
    # print(df["Abbr"].iloc[2])
    boy = df.loc[df['Abbr']=='CA'].index
    print(df["State"].iloc[boy])

    # nav_user_registration(driver)
    # new_user(driver, True, 2, ["User", "Password"], "Email", ["Jaden", "Syre", "Smith"],
    #          ["Address", "San Francisco", "Sasketchewan", "00000", "7777777777"])

    # driver = webdriver.Chrome()
    # driver.get('https://python-forum.io/Thread-Need-Help-Opening-A-New-Tab-in-Selenium')
    # # Open a new window
    # # This does not change focus to the new window for the driver.
    # driver.execute_script("window.open('http://www.google.com/');")
    # time.sleep(3)
    # # Switch to the new window
    # driver.switch_to.window(driver.window_handles[1])
    # driver.get("http://stackoverflow.com")
    # time.sleep(3)
    # # close the active tab
    # driver.close()
    # time.sleep(3)
    # # Switch back to the first tab
    # driver.switch_to.window(driver.window_handles[0])
    # driver.get("http://google.se")
    # time.sleep(3)
    # # Close the only tab, will also close the browser.
    # driver.close()




'''
# df = pd.read_csv("name-abbr.csv", names=["State", "Abbr"], header=None)
# print(df["Abbr"].iloc[2])

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