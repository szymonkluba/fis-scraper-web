import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_dynamic_content(url):

    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    path = os.path.dirname(os.path.realpath(__file__)) + "/driver/chromedriver"

    driver = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
    driver.get(url)
    sleep(2)
    return driver.page_source
