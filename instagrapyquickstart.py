# import urllib
import re
import requests
import pandas as pd
import instagrapy.igpost as igpost
import instagrapy.iguser as iguser
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from time import sleep
import time
import instagrapy.util as util


# posturl = "BsFFVTMFJ2i"
# postlink = "https://www.instagram.com/p/" + posturl

# postlike_list = get_postlike(posturl)

username = "username"
password = "password"
baseurl = "http://www.instagram.com/"

userurl = baseurl + username

driver = util.browser_start()
util.ig_login_process(driver, username, password)




time.sleep(100000)

driver = util.ig_login(driver, username, password)

#followerlist = iguser.get_follower_account(driver, "nakhalphotography")
#followinglist = iguser.get_following_account(driver, "nakhalphotography")

#notfollowbacklist = set(followinglist) - set(followerlist)

#util.save("notfollowback", notfollowbacklist)


a = igpost.get_postlike_account(driver, test1)


# more than 100 likes
test2 = "B0Ls6WlF2Al"  # less than 10 likes

driver.get("https://www.instagram.com/p/B0Ls6WlF2Al")

a = igpost.get_postlike_account(driver, test1)

pb = driver.find_element_by_xpath(
    '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]')
total_postlike = int(driver.find_element_by_xpath(
    '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]/span').text)
print(total_postlike)

a = igpost.check_postlike(driver, "B0HkbRiHATc")

if not a:
    result = igpost.like_post(driver, "B0HkbRiHATc")
else:
    result = "Error"

print(result)

tmp = iguser.get_userpost(driver, username, 44)

chrome_options = Options()

chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('--dns-prefetch-disable')
chrome_options.add_argument('--lang=en-US')
chrome_options.add_argument('--disable-setuid-sandbox')
capabilities = DesiredCapabilities.CHROME

user_agent = "Chrome"
chrome_options.add_argument('user-agent={user_agent}'
                            .format(user_agent=user_agent))
chrome_prefs = {
    'intl.accept_languages': 'en-US'
}

chrome_options.add_experimental_option('prefs', chrome_prefs)
driver = webdriver.Chrome(desired_capabilities=capabilities,
                          chrome_options=chrome_options)

# driver = webdriver.Chrome(chrome_options=options)


driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

unform = driver.find_element_by_xpath("//input[@name='username']")
unform.send_keys(username)

unform = driver.find_element_by_xpath("//input[@name='password']")
unform.send_keys(password)

time.sleep(5)

login_button = driver.find_element_by_xpath(
    '//main[@role = "main"]/div[1]/article[1]/div[1]/div[1]/div[1]/form[1]/div[4]/button')
login_button.click()

time.sleep(5)

# tmp = iguser.get_latestuserpost(username)

tmp = iguser.get_userpost(driver, username, 44)

tmp = iguser.get_latestuserpost(username)
