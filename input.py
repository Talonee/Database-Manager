from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd



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
    # for i in range(5):
    
    element = driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/a")
    element.click()

    ay = driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[2]/a")
    ay.click()
    
    # driver.get('https://victorvalley.parkadmin.com/admin/start/main.aro')
    


    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # driver.close()

def new_user(driver, active, user, account, email, name, address):
    # Active status
    if active:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[3]/td/input").click()        

    # User Type
    driver.find_element_by_id("tst_selectUserType").click()
    if user == 1:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[2]").click()
    elif user == 2:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[3]").click()
    elif user == 3:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[4]").click()
    elif user == 4:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[5]").click()
    elif user == 5:
        driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[4]/td/select/option[6]").click()

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
    driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[15]/td/input").send_keys(address[1])
    driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[16]/td/select").click()
    driver.find_element_by_xpath("/html/body/div[1]/form/table[2]/tbody[1]/tr[16]/td/select").send_keys(address[2])
    driver.find_element_by_id("tst_postalCode").send_keys(address[3])
    driver.find_element_by_id("tst_localPhoneNumber").send_keys(address[4])


if __name__ == "__main__":
    driver = login()
    nav_user_registration(driver)

    new_user(driver, True, 2, ["User", "Password"], "Email", ["Jaden", "Syre", "Smith"],
            ["Address", "San Francisco", "Sasketchewan", "00000", "7777777777"])


    # df = pd.read_csv("name-abbr.csv", names=["State", "Abbr"], header=None)
    # states = {}
    # for i in range(df.shape[0]):
    #     states[df.iloc[i, 0]] = df.iloc[i, 1]


# TODO:
# Create a class for each person, attributes are linked to their entries
# Somehow gain access to SID/FID
# Go through each person and register an account for them
# Remove all void/empty entries