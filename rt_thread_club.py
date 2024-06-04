#-*- coding:utf8 -*-
import os
import sys
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By

def login_in_club(user_name, pass_word):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    driver = webdriver.Chrome(options=option)
    driver.maximize_window()
    # login in
    driver.get("https://www.rt-thread.org/account/user/index.html?response_type=code&authorized=yes&scope=basic&state=1588816557615&client_id=30792375&redirect_uri=https://club.rt-thread.org/index/user/login.html")
    element = driver.find_element(by=By.ID,value='username')
    element.send_keys(user_name)
    element = driver.find_element(by=By.ID,value='password')
    element.send_keys(pass_word)
    driver.find_element(by=By.ID,value='login').click()
    time.sleep(10)

    current_url = driver.current_url
    if current_url != "https://club.rt-thread.org/":
        logging.error("username or password error, please check it, login in failed!");
        sys.exit(1)
    try:
        element = driver.find_element(by=By.LINK_TEXT,value=u"立即签到")
    except Exception as e:
        logging.info("Signed in today! or an error message : {0}".format(e))
    else:
        element.click()
        logging.info("Sign in success!")

    time.sleep(1)

    day_num = None
    # check sign in days
    try:
        element = driver.find_element(by=By.PARTIAL_LINK_TEXT,value=u"今日已签到")
    except Exception as e:
        logging.error("Error message : {0}".format(e))
    else:
        day_num = element.text
        logging.info("signed in today : {0}".format(day_num))
        driver.find_element(by=By.LINK_TEXT,value='排行榜').click()
        time.sleep(5)
        driver.get_screenshot_as_file("/home/runner/paihang.png")
        driver.quit()
    return day_num
