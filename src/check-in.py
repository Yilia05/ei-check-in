# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
import time
from selenium.webdriver.support.ui import Select
import datetime
import sys
import logging
import os

'''
Author: Hang Hu
Github: https://github.com/Hang-Hu
Welcome to join and leave you information here
'''


def apply(date, driver):
    driver.get("http://www.ebay-hr-system.com/eleave/")

    # username and password for login
    driver.find_element_by_id("userid").send_keys("I2430")
    driver.find_element_by_id("pwd").send_keys("hu87...hu")
    driver.find_element_by_css_selector(".buttonstyle").click()

    # hover dropdown menu: my application
    element_to_hover = driver.find_element_by_id("menu_11001169")
    hover = ActionChains(driver).move_to_element(element_to_hover)
    hover.perform()

    # click one link in the dropdown menu
    driver.find_element_by_id("menu_11001170").click()

    print("siwtch to frame")
    # switch to KFrame
    iframe = driver.find_element_by_id('KFrame')
    driver.switch_to_frame(iframe)
    print("finish switching to frame")
    # hover to another place so that last hover will be canceled
    element_to_hover = driver.find_element_by_xpath(
        '//*[@id="form1"]/div[2]/div/div[2]/div[3]')
    hover = ActionChains(driver).move_to_element(element_to_hover)
    hover.perform()

    # click into the page
    driver.find_element_by_xpath(
        '//*[@id="form1"]/div[2]/div/div[2]/div[1]').click()
    driver.find_element_by_xpath(
        '//*[@id="form1"]/div[2]/div/div[2]/div').click()

    # send date
    driver.find_element_by_id("F1_1_C6").send_keys(date)

    # select start time: morning
    select = Select(driver.find_element_by_id("F1_1_C11"))
    select.select_by_value("1")

    # select end time: afternoon
    select = Select(driver.find_element_by_id("F1_1_C12"))
    select.select_by_value("2")

    # submit application
    driver.find_element_by_xpath(
        '//*[@id="funcPanel"]/div[1]/div/div[2]/a').click()
    print("accept alert.")
    alert = driver.switch_to_alert()
    alert.accept()
    '''
    js = """
    window.alert = function(message) {
    lastAlert = message;
    }
    """
    driver.execute_script("%s" % js)
    '''
    print("finish accepting alert.")
    # driver.close()
    if "不能重复提交" in driver.page_source:
        return False
    else:
        return True


def openbrowser():
    #driver = webdriver.PhantomJS()
    driver=webdriver.Chrome()
    driver.set_window_size(1120, 550)
    return driver

os.environ['NO_PROXY'] = '127.0.0.1'
logging.basicConfig(filename='check-in.log', level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    datefmt='%m %d, %Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(console)
logger.info("Logs supported.")
# set encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')
# set date you want to apply
startdate = "2017-08-21"  # inclusive
length = 3  # number of days to be checked in
dateformate = "%Y-%m-%d"
startdate = datetime.datetime.strptime(startdate, dateformate).date()
driver = openbrowser()

for i in xrange(0, length, 1):
    date = startdate + datetime.timedelta(days=i)
    if date.isoweekday() in range(1, 6):
        date = date.strftime(dateformate)
        while True:
            try:
                result = apply(date, driver)
            except NoSuchWindowException as e:
                driver = openbrowser()
            except Exception as e:
                logger.error("Exception occurs: " + str(e.__class__) + str(e))
                driver.save_screenshot('exception.png')
            else:
                logger.info(date + " " + str(result))
                break
    else:
        logger.info(str(date) + " " + str(date.isoweekday()) +
                    " is not a weekday")
driver.close()
