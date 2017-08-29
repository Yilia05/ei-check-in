# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support.ui import Select
import datetime
import logging
import os
import json
import argparse
'''
Author: Hang Hu
Github: https://github.com/Hang-Hu
Welcome to join and leave you information here
'''

def parArg():
    parser = argparse.ArgumentParser(
        description='Auto check in for eBay intern in Shanghai.')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')
    subparsers = parser.add_subparsers(help='sub-command help', dest='command')
    mul_parser = subparsers.add_parser('mul', help='Check in for multiple days.')
    mul_parser.add_argument('-d', action='store', dest='startdate',
                        help='The first day to be checked in, format is YYYY-mm-dd such as 2017-08-29.',
                        required=True)
    mul_parser.add_argument('-l', action='store', dest='length',
                        help='The number of days to be checked in.',
                        required=True)
    # mul_parser.set_defaults(which='mul')
    '''action='version' is required for version function'''
    today_parser = subparsers.add_parser('today', help='Check in for today.')
    # mul_parser.set_defaults(which='today')
    args = parser.parse_args()
    if args.command == 'mul':
        apply_more(args.startdate, int(args.length))
    elif args.command == 'today':
        apply_more(datetime.datetime.today().strftime('%Y-%m-%d'), 1)


def readSecret():
    with open('secret.json') as secret_file:
        secret = json.load(secret_file)

    return secret["username"], secret["password"]


def apply(date, driver):
    driver.get("http://www.ebay-hr-system.com/eleave/")
    username, password = readSecret()
    # username and password for login
    driver.find_element_by_id("userid").send_keys(username)
    driver.find_element_by_id("pwd").send_keys(password)
    driver.find_element_by_css_selector(".buttonstyle").click()

    # hover dropdown menu: my application
    element_to_hover = driver.find_element_by_id("menu_11001169")
    hover = ActionChains(driver).move_to_element(element_to_hover)
    hover.perform()

    # click one link in the dropdown menu
    driver.find_element_by_id("menu_11001170").click()

    # switch to KFrame
    iframe = driver.find_element_by_id('KFrame')
    driver.switch_to_frame(iframe)
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
    # driver.close()
    if "不能重复提交" in driver.page_source:
        return 'has already been checked in, can not be checked in twice.'
    else:
        return 'is checked in successfully.'


def openbrowser():
    # driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    driver.set_window_size(1120, 550)
    return driver


def apply_more(startdate, length):
    os.environ['NO_PROXY'] = '127.0.0.1'
    logging.basicConfig(filename='check-in.log', level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%m %d, %Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.addHandler(console)
    # set encoding=utf8
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    # set date you want to apply
    # startdate, length = parArg()
    # startdate = "2017-08-29"  # inclusive
    # length = 1  # number of days to be checked in
    dateformate = "%Y-%m-%d"
    startdate = datetime.datetime.strptime(startdate, dateformate).date()
    driver = openbrowser()

    for i in range(0, length, 1):
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


parArg()
