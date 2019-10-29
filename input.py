from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()
driver.get('https://victorvalley.parkadmin.com/admin/start/login.aro')

with open("login.txt") as f:
    f = f.read().splitlines()
    un = f[0]
    pw = f[1]

# print(driver.current_url)

id_box = driver.find_element_by_id("username")
id_box.send_keys(un)

pass_box = driver.find_element_by_id("password")
pass_box.send_keys(pw)

login_button = driver.find_element_by_id("login")
login_button.click()

element = driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/a")
hover = ActionChains(driver).move_to_element(element)
hover.perform()

driver.implicitly_wait(3)

ay = driver.find_element_by_xpath("/html/body/nav/div/div[2]/ul[1]/li[1]/ul/li[3]/a")
ay.click()
