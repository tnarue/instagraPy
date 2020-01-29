import re
import requests
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from time import sleep
import time
import instagrapy.util as util
import instagrapy.iguser as iguser



def unfollow_from_list(driver, unfollowlist, n, timewait):
    for i in unfollowlist:
        if i % n == 0:
            time.sleep(timewait)
        iguser.unfollow_user(driver, i)

