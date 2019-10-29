import selenium
from selenium import webdriver

# driver = webdriver.Chrome()

# driver.get('https://victorvalley.parkadmin.com/admin/start/login.aro')

with open("login.txt") as f:
    f = f.read().splitlines()
    un = f[0]
    pw = f[1]


# print(driver.current_url)

# id_box = driver.find_element_by_id("username")
# id_box.send_keys(un)

# pass_box = driver.find_element_by_id("password")
# pass_box.send_keys(pw)

# login_button = driver.find_element_by_id("login")
# login_button.click()

# print(driver.current_url)