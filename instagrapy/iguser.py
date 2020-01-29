import re
import requests
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
from time import sleep
import time
import instagrapy.util as util
import pickle


# Check if user is already followed, return True. Otherwise return False.
def check_userfollow(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    try:
        follow_text = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/div[1]/div[1]/span[1]/span[1]/button[1]').text
    except NoSuchElementException:
        print("Check Follow Error: Follow Text not found")
        return True
    if follow_text == "Follow":
        return False
    else:
        return True


# Follow user if user is not followed yet
def follow_user(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    if not check_userfollow(driver, username):
        try:
            follow_button = driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/header[1]/section[1]/div[1]/div[1]/span[1]/span[1]/button[1]')
            follow_button.click()
            return "Follow Success"
        except NoSuchElementException:
            return "Follow Error: Like Button Not Found"
    else:
        return "User is already followed"


# Unfollow user if user is already followed
def unfollow_user(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    if check_userfollow(driver, username):
        try:
            unfollow_button = driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/header[1]/section[1]/div[1]/div[1]/span[1]/span[1]/button[1]')
            unfollow_button.click()
            return "UnFollow Success"
        except NoSuchElementException:
            return "UnFollow Error: Like Button Not Found"
    else:
        return "User is already followed"


# return number of followers
def get_follower_count(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    try:
        follower_count = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[2]/a[1]/span[1]').text.replace(',', '')
        return int(follower_count)
    except NoSuchElementException:
        print("Can't get number of followers")
        return 0


# return number of followers
def get_following_count(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    try:
        following_count = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]/span[1]').text.replace(',', '')
        return int(following_count)
    except NoSuchElementException:
        print("Can't get number of followings")
        return 0


def get_follower_account(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    total_follower = get_follower_count(driver, username)
    time.sleep(7)

    if not util.check_pathexist_by_xpath(driver, '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[2]/a[1]'):
        driver.get(userurl)
        time.sleep(10)
        print("1.1")

    try:
        if driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[2]/a[1]/span').text != "followers":
            driver.get(userurl)
            time.sleep(10)
            print("1.2")

        print("Already Get Number of Followers")
        pb = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[2]/a[1]')
        # scroll postlike box
        pb.click()
        print("Already Click Follower Box")
        time.sleep(5)
        tmp = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]')
        print("Already get scroll box")
        follower_list = []
        check = 0
        checkvalue = 0
        loaded_till_now = 0
        while loaded_till_now < total_follower and check < 50:
            # scroll down
            if loaded_till_now > 0:
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', tmp)
            time.sleep(5)
            # scrape postlike box (box contains list of div of accounts)
            elem = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]/ul[1]/div[1]')
            # text_content = wait(driver, 10).until(lambda driver: elem.text)

            # wait till loaded and scrape links in postlike (including account link)
            time.sleep(check * 10)
            text_content = wait(driver, 20).until(lambda driver: elem.find_elements_by_css_selector('a'))

            for i in text_content:
                # get the title of IG accounts who like this post
                temp = i.get_attribute("title")
                # ignore if title is blank or = Follow (Follow Button), get only account name
                if temp != '' and (temp not in follower_list):
                    follower_list.append(temp)

            loaded_till_now = len(follower_list)

            if len(follower_list) > 0 and checkvalue == loaded_till_now:
                check = check + 1
            elif check > 1 and checkvalue < loaded_till_now:
                check = 0
                checkvalue = loaded_till_now
            else:
                checkvalue = loaded_till_now

            print("get follower loadtillnow: ", loaded_till_now, "totalfollower: ", total_follower, "check: ", check)

        print("Get followers completed")
        return follower_list
    except NoSuchElementException:
        print("Can't get followers")
        # print(pb)
        return None


def get_following_account(driver, username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username

    if not util.check_pathexist_by_xpath(driver, '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]'):
        driver.get(userurl)
        print("2.1")

    try:
        if driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]/span').text != "following":
            driver.get(userurl)
            print("2.2")

        total_following = get_following_count(driver, username)
        print("Already Get Number of Followers")
        time.sleep(7)
        pb = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[3]/a[1]')
        # scroll postlike box
        pb.click()
        print("Already Click Follower Box")
        time.sleep(5)
        tmp = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]')
        print("Already get scroll box")
        following_list = []
        check = 0
        checkvalue = 0
        loaded_till_now = 0
        while loaded_till_now < total_following and check < 50:
            # scroll down
            if loaded_till_now > 0:
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', tmp)
            time.sleep(5)
            # scrape postlike box (box contains list of div of accounts)
            elem = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]/ul[1]/div[1]')
            # text_content = wait(driver, 10).until(lambda driver: elem.text)

            # wait till loaded and scrape links in postlike (including account link)
            time.sleep(check * 10)
            text_content = wait(driver, 20).until(lambda driver: elem.find_elements_by_css_selector('a'))

            for i in text_content:
                # get the title of IG accounts who like this post
                temp = i.get_attribute("title")
                # ignore if title is blank or = Follow (Follow Button), get only account name
                if temp != '' and (temp not in following_list):
                    following_list.append(temp)

            loaded_till_now = len(following_list)

            if len(following_list) > 0 and checkvalue == loaded_till_now:
                check = check + 1
            elif check > 1 and checkvalue < loaded_till_now:
                check = 0
                checkvalue = loaded_till_now
            else:
                checkvalue = loaded_till_now

            print("get following loadtillnow: ", loaded_till_now, "totalfollower: ", total_following, "check: ", check)

        # print(text_content)
        print("Test4")
        return following_list
    except NoSuchElementException:
        print("Can't get followers")
        return None


def get_notfollowback_account(driver, username):
    follower_list = get_follower_account(driver, username)
    following_list = get_following_account(driver, username)
    return set(following_list) - set(follower_list)


def get_fan_account(driver, username):
    follower_list = get_follower_account(driver, username)
    following_list = get_following_account(driver, username)
    return set(follower_list) - set(following_list)


def get_mutual_account(driver, username):
    follower_list = get_follower_account(driver, username)
    following_list = get_following_account(driver, username)
    mutual_account = [account for account in follower_list if account in following_list]
    return mutual_account


# Get 9 latest post id of a user
def get_latestuserpost(username):
    # get 9 latest posts
    userlink = "https://www.instagram.com/" + username
    result = requests.get(userlink)
    tmp = result.content.decode('ISO-8859-1')
    postid = re.findall(r'[\"]shortcode[\"]:[\"]([a-zA-Z0-9]{11})[\"]', tmp)
    return postid


# Get post id of a user for exact amount
def get_userpost(driver, username, numberofpost):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver.get(userurl)
    try:
        # login xpath '//div[@role="dialog"]/article[1]/div[2]/section[2]/div[1]/div[2]/button[1]'
        tmp = driver.find_element_by_xpath('//main[@role = "main"]/div[1]/div[2]/article[1]/div[1]/div[1]')
        sleep(3)
        # login xpath '//div[@role="dialog"]/article[1]/div[2]/section[2]/div[1]/div[2]/button[1]/span'

        login_path = '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[1]/span/span'
        nonlogin_path = '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[1]/a[1]/span'
        postidlist = []
        check = 0
        checkvalue = 0
        loaded_till_now = 0
        while loaded_till_now < numberofpost and check < 5:
            # scroll down
            if loaded_till_now > 0:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);', tmp)
            # wait till loaded and scrape links in postlike (including account link)
            time.sleep(check * 10 + 5)
            elem = driver.find_element_by_xpath('//main[@role = "main"]/div[1]/div[2]/article[1]/div[1]/div[1]')
            text_content = wait(driver, 20).until(lambda driver: elem.find_elements_by_css_selector('a'))

            for i in text_content:
                # get the title of IG accounts who like this post
                tmp = i.get_attribute("href")
                postid = re.findall(r'/p/([\S]{11})', tmp)

                if postid:
                    if postid[0] != '' and postid[0] not in postidlist:
                        postidlist.append(postid[0])
                        loaded_till_now = len(postidlist)

                if loaded_till_now >= numberofpost:
                    break

            if loaded_till_now > 0 and (checkvalue == loaded_till_now):
                check = check + 1
            elif check > 0 and checkvalue < loaded_till_now:
                checkvalue = loaded_till_now
                check = 0
            else:
                checkvalue = loaded_till_now

            print("loadtillnow: ", loaded_till_now, "totalpostlike: ", total_post, "check: ", check, "checkvalue: ",
                  checkvalue)
        driver.quit()
        return postidlist
    except NoSuchElementException:
        print("No Element")
        driver.quit()
        return None


# Get post id of all post by a user
def get_alluserpost(username):
    baseurl = "http://www.instagram.com/"
    userurl = baseurl + username
    driver = webdriver.Chrome()
    driver.get(userurl)
    try:
        # login xpath '//div[@role="dialog"]/article[1]/div[2]/section[2]/div[1]/div[2]/button[1]'
        tmp = driver.find_element_by_xpath('//main[@role = "main"]/div[1]/div[2]/article[1]/div[1]/div[1]')
        sleep(3)
        # login xpath '//div[@role="dialog"]/article[1]/div[2]/section[2]/div[1]/div[2]/button[1]/span'
        total_post = int(driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/header[1]/section[1]/ul[1]/li[1]/a[1]/span').text)
        postidlist = []
        check = 0
        checkvalue = 0
        loaded_till_now = 0
        while loaded_till_now < total_post and check < 5:
            # scroll down
            if loaded_till_now > 0:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);', tmp)
            # wait till loaded and scrape links in postlike (including account link)
            time.sleep(check * 10 + 5)
            elem = driver.find_element_by_xpath('//main[@role = "main"]/div[1]/div[2]/article[1]/div[1]/div[1]')
            text_content = wait(driver, 20).until(lambda driver: elem.find_elements_by_css_selector('a'))

            for i in text_content:
                # get the title of IG accounts who like this post
                tmp = i.get_attribute("href")
                postid = re.findall(r'/p/([\S]{11})', tmp)

                if postid:
                    if postid[0] != '' and postid[0] not in postidlist:
                        postidlist.append(postid[0])

            loaded_till_now = len(postidlist)

            if loaded_till_now > 0 and (checkvalue == loaded_till_now):
                check = check + 1
            elif check > 0 and checkvalue < loaded_till_now:
                checkvalue = loaded_till_now
                check = 0
            else:
                checkvalue = loaded_till_now

            print("loadtillnow: ", loaded_till_now, "totalpostlike: ", total_post, "check: ", check, "checkvalue: ",
                  checkvalue)
        driver.quit()
        return postidlist
    except NoSuchElementException:
        print("No Element")
        driver.quit()
        return None
