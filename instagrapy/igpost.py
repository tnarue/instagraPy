from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait as wait
import instagrapy.util as util
from time import sleep
import time


# get number of likes of a post
def get_postlike_count(driver, postid):
    posturl = "https://www.instagram.com/p/" + postid
    if util.check_pathexist_by_xpath(driver,
                                     '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]'):
        x = int(driver.find_element_by_xpath(
            '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]/span').text.replace(',',
                                                                                                                    ''))
        return x + 1
    elif util.check_pathexist_by_xpath(driver,
                                       '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[1]/a[1]'):
        return int(driver.find_element_by_xpath(
            '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[1]/a[1]/span').text.replace(',',
                                                                                                                    ''))
    else:
        return 0


def get_post_owner_username(driver, postid):
    baseurl = "https://www.instagram.com/p/"
    posturl = baseurl + postid
    print("Test1")
    driver.execute_script("window.open('', '__blank');")
    print("Test2")
    time.sleep(3)
    print("Test3")
    driver.get(posturl)
    print("Test4")
    time.sleep(5)
    try:
        elem = driver.find_element_by_xpath(
            '//main[@role="main"]/div[1]/div[1]/article[1]/header[1]/div[2]/div[1]/div[1]/h2[1]/a[1]')
        username = elem.get_attribute("title")
        print("Test5")
        return username
    except NoSuchElementException:
        print("Test6")
        return "Error"


# get list of username who like a post
def get_postlike_account(driver, postid):
    start_time = time.time()
    posturl = "https://www.instagram.com/p/" + postid
    driver.get(posturl)
    try:
        # login xpath '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]/
        # non-login xpath  '//main[@role = "main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[1]/a[1]'
        pb = driver.find_element_by_xpath(
            '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]')
        # login xpath '//main[@role="main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[2]/a[2]/span'
        # non-login xpath '//main[@role = "main"]/div[1]/div[1]/article[1]/div[2]/section[2]/div[1]/div[1]/a[1]/span'
        total_postlike = get_postlike_count(driver, postid)
        print(total_postlike)
        print(type(total_postlike))
        driver.execute_script("arguments[0].click();", pb)
        time.sleep(0.2)
        print("Test2")
        # scroll postlike box
        tmp = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]/div[1]')
        sleep(3)
        # driver.execute_script("arguments[0].scrollIntoView();", tmp)
        titlelist = []
        check = 0
        checkvalue = 0
        loaded_till_now = 0
        while loaded_till_now < total_postlike and check < 5:
            # scroll down
            if loaded_till_now > 0:
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', tmp)
            time.sleep(5)
            # scrape postlike box (box contains list of div of accounts)
            elem = driver.find_element_by_xpath('//div[@role = "dialog"]/div[2]/div[1]/div[1]')
            # text_content = wait(driver, 10).until(lambda driver: elem.text)

            # wait till loaded and scrape links in postlike (including account link)
            time.sleep(check * 10)
            text_content = wait(driver, 20).until(lambda driver: elem.find_elements_by_css_selector('a'))

            for i in text_content:
                # get the title of IG accounts who like this post
                temp = i.get_attribute("title")
                # ignore if title is blank or = Follow (Follow Button), get only account name
                if temp != '' and (temp not in titlelist):
                    titlelist.append(temp)

            loaded_till_now = len(titlelist)

            if len(titlelist) > 0 and checkvalue == loaded_till_now:
                check = check + 1
            elif check > 1 and checkvalue < loaded_till_now:
                check = 0
                checkvalue = loaded_till_now
            else:
                checkvalue = loaded_till_now

            print("loadtillnow: ", loaded_till_now, "totalpostlike: ", total_postlike, "check: ", check)

        # print(text_content)
        print(titlelist)
        return titlelist
    except NoSuchElementException:
        print("No Element")
        # print(pb)
        return None


# check if post is already liked, return true. If post is not liked yet, return false.
def check_postlike(driver, postid):
    posturl = "https://www.instagram.com/p/" + postid
    driver.get(posturl)

    try:
        like_text = driver.find_element_by_xpath(
            '//main[@role = "main"]/div[1]/div[1]/article[1]/div[2]/section[1]/span[1]/button[1]/span')
        post_status = like_text.get_attribute("aria-label")
    except NoSuchElementException:
        print("Check Postlike Error: Like Text not found")
        return True

    if post_status == "Unlike":
        return True
    else:
        return False


# like post if post is not liked yet
def like_post(driver, postid):
    posturl = "https://www.instagram.com/p/" + postid
    driver.get(posturl)
    if not check_postlike(driver, postid):
        try:
            like_button = driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/div[1]/article[1]/div[2]/section[1]/span[1]/button[1]')
            like_button.click()
            return "Like Success"
        except NoSuchElementException:
            return "Like Post Error: Like Button Not Found"
    else:
        return "Post is already liked"


# unlike post if post is already liked
def unlike_post(driver, postid):
    posturl = "https://www.instagram.com/p/" + postid
    driver.get(posturl)
    if check_postlike(driver, postid):
        try:
            like_button = driver.find_element_by_xpath(
                '//main[@role = "main"]/div[1]/div[1]/article[1]/div[2]/section[1]/span[1]/button[1]')
            like_button.click()
            return "Unlike Success"
        except NoSuchElementException:
            return "Unlike Post Error: Like Button Not Found"
    else:
        return "Post " + postid + "Is Not Liked Yet"


# return list of user who comment post
def get_postcomment(driver, postid):
    posturl = "https://www.instagram.com/p/" + postid
    driver.get(posturl)
    return None
