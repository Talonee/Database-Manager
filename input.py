from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

import pandas as pd
import time

# Login database with credentials
def login():
    #### Google Chrome
    # driver = webdriver.Chrome()
    # driver.get('https://victorvalley.parkadmin.com/admin/start/login.aro')
    
    #### Firefox
    binary = r'C:\Users\Talon.Pollard\AppData\Local\Mozilla Firefox\firefox.exe' # Work dir
    # binary = r'C:\Program Files\Mozilla Firefox\firefox.exe' # Home dir
    options = Options()
    # options.set_headless(headless=True)
    options.binary = binary

    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0")

    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = True #optional

    driver = webdriver.Firefox(firefox_profile=profile, options=options, capabilities=cap, executable_path="drivers/geckodriver.exe")
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

# Navigate to User Registration category
def nav_user_registration(driver):
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/a")
    click("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[2]/a")

# Register new users
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

# Navigate to User Search category and proceed to edit
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
        print("Current page: {}".format(page))
        # View number of users currently presented
        num_users = driver.execute_script("return document.getElementsByTagName('tr').length") - 9
    
        # Since some users relocate after being edited, 
        # this loop ensures all entries are properly considered
        i = 1
        while i <= num_users:
            # Find and edit users
            username = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[3]/a".format(i)).text
            if username in names or username + " - invalid address" in names: 
            # if username in names: # iteration for invalid addresses
                i += 1
            else:
                curr_name = edit_user(i, username, names)
                new_users.append(curr_name)
                names.append(curr_name)
            
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                driver.refresh() # Refresh webpage
                i += 1 # iteration for invalid addresses

        # Reset existing usernames if response is no, else append
        store_users(new_users, True) if response == "n" else store_users(new_users)
        new_users = []
        page += 1
    
# Permission to access preexisting list of usernames
def storage_response():
    print("Would you like to read in existing user names? y/n")
    response = "y"
    while response != "y" and response != "n":
        print("Invalid response. Please respond with y/n")
        response = input()

    # Read existing usernames if response is yes, else nothing
    names = read_users() if response == "y" else []

    return names, response

# Edit user profile
def edit_user(i, username, names):
    df = pd.read_csv("Work files/name-abbr.csv", names=["State", "Abbr"], header=None, index_col=0)

    address = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[5]".format(i)).text
    city = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/table/tbody/tr[{}]/td[6]".format(i)).text

    # Open Mr. Google and search address
    driver.execute_script("window.open('http://www.google.com/');")
    driver.switch_to.window(driver.window_handles[1])
    search = driver.find_element_by_name('q')
    search.send_keys("{} {}".format(address, city))
    search.send_keys(Keys.RETURN)
    time.sleep(1)

    # Run iff Mr. Google returns a valid address
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
        print("Editing user: {}".format(username))
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
        print("Username: {}\nAddress: {}, {}".format(username, address, city))
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

def nav_violation_entry():
    click("/html/body/nav/div/div[2]/ul[1]/li[2]/a")
    click("/html/body/nav/div/div[2]/ul[1]/li[2]/ul/li[2]/a")
    time.sleep(0.75)

    # Select writer
    writer = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="writer"]'))
    for i in writer.options:
        if "noreen" in i.text.lower():
            writer.select_by_visible_text(i.text)

    # Select spoiled - This section is to be determined what spoiled means
    # 0 - Valid - not spoiled
    # 1 - Spoiled
    # 2 - Drive Away
    # 3 - TESTING
    spoil = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="SpoilID"]'))
    for i in spoil.options:
        if "testing" in i.text.lower():
            spoil.select_by_visible_text(i.text)

    # Ticket number
    tix_no = driver.find_element(By.CSS_SELECTOR, 'input[name="ticket"]').send_keys("0000000")
    
    # Warning check
    warning = False
    if warning:
        warn_btn = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="btn_setAsWarning"]').click()

    # Ticket type
    tix_type = Select(driver.find_element(By.CSS_SELECTOR, 'select[name="TicketType"]'))
    for i in tix_type.options:
        if "Municipal":
            tix_type.select_by_visible_text("Municipal")
        else:
            tix_type.select_by_visible_text("Private Property")


    

    

    time.sleep(5)

if __name__ == "__main__":
    driver = login()
    nav_violation_entry()
    driver.quit()
    
    # nav_user_search()
    # nav_user_registration(driver)
    # new_user(driver, True, 2, ["User", "Password"], "Email", ["Jaden", "Syre", "Smith"],
    #          ["Address", "San Francisco", "Sasketchewan", "00000", "7777777777"])


