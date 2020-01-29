from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from time import sleep
from selenium.webdriver.common.by import By
import time
from collections import defaultdict
import string
import pandas as pd
import sys
from fake_useragent import UserAgent

_NoneType = type(None)

def browser_start():
    chrome_options = Options()

    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('--lang=en-US')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("user-data-dir=selenium2")
    user_agent = "Chrome"
    chrome_options.add_argument('user-agent={user_agent}'
                                .format(user_agent=user_agent))
    capabilities = DesiredCapabilities.CHROME

    chrome_prefs = {
        'intl.accept_languages': 'en-US'
    }

    chrome_options.add_experimental_option('prefs', chrome_prefs)
    driver = webdriver.Chrome(desired_capabilities=capabilities,
                              chrome_options=chrome_options,
                              executable_path='/Users/naruethait/Documents/PythonWork/instagrapy/assets/chromedriver')
    return driver


def ig_login_process(driver, username, password):
    check_login_value = check_login(driver, username)
    if check_login_value == 0:
        return driver
    elif check_login_value == 1:
        ig_logout(driver)
        time.sleep(3)
        ig_login(driver, username, password)
        return driver
    elif check_login_value == 2:
        ig_login(driver, username, password)
        return driver
    else:
        print("Problem Login")
        sys.exit(1)


# close all tabs except the first tab
def browser_closealltabs(driver):
    n = len(driver.window_handles)
    i = n-1
    while i > 0:
        driver.switch_to_window(driver.window_handles[i])
        driver.close()
        i = i-1
    return driver.switch_to_window(driver.window_handles[0])


def check_login(driver, username):
    driver.get("https://www.instagram.com/")
    time.sleep(3)
    try:
        currentuser = driver.find_element_by_xpath("//main[@role='main']/section[1]/div[3]/div[1]/div[1]/div[2]/div[1]").text
        print("current username: " + currentuser)
        if currentuser == username:
            print("Already Logged In")
            return 0
        elif currentuser != username:
            print("Login As Other User")
            return 1
    except NoSuchElementException:
        print("Not Yet Log In")
        return 2


def ig_login(driver, username, password):

    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    unform = driver.find_element_by_xpath("//input[@name='username']")
    unform.send_keys(username)

    unform = driver.find_element_by_xpath("//input[@name='password']")
    unform.send_keys(password)

    time.sleep(5)

    login_button = driver.find_element_by_xpath('//button[@type = "submit"]')
    login_button.click()

    time.sleep(5)
    check_login(driver, username)
    return driver


def ig_logout(driver):
    baseurl = "https://www.instagram.com/"
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    try:
        currentuser = driver.find_element_by_xpath(
            "//main[@role='main']/section[1]/div[3]/div[1]/div[1]/div[2]/div[1]").text
    except NoSuchElementException:
        print("Error: Can't Log Out")
        return

    userurl = baseurl + currentuser
    driver.get(userurl)
    time.sleep(5)
    if check_pathexist_by_xpath(driver, "//main[@role='main']/div[1]/header[1]/section[1]/div[1]/div[1]/button[1]"):
        settingbutton = driver.find_element_by_xpath(
        "//main[@role='main']/div[1]/header[1]/section[1]/div[1]/div[1]/button[1]")
        settingbutton.click()
        time.sleep(5)
        if check_pathexist_by_xpath(driver, "//div[@role='dialog']/div[1]/div[1]/button[7]"):
            logout_button = driver.find_element_by_xpath("//div[@role='dialog']/div[1]/div[1]/button[7]")
            logout_button.click()
            return driver
        else:
            print("Logout Button Not Found")
            return
    else:
        print("Setting Button Not Found")
        return


def check_pathexist_by_xpath(driver, path):
    try:
        driver.find_element_by_xpath(path)
        return True
    except NoSuchElementException:
        return False


def save(name, savelist):
    filename = name + ".csv"
    df = pd.DataFrame(savelist, columns=["column"])
    df.to_csv(filename, index=False)
