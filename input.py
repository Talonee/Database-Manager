from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys




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
    
    driver.get('https://victorvalley.parkadmin.com/admin/start/main.aro')
    

    
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # driver.close()

if __name__ == "__main__":
    driver = login()
    nav_user_registration(driver)