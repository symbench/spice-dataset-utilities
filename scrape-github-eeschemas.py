import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def login(driver, username, password):
    field = driver.find_element_by_id('login_field')
    field.send_keys(username)
    field = driver.find_element_by_id('password')
    field.send_keys(password)
    btn = driver.find_element_by_xpath("//input[@type='submit']")
    btn.click()
    time.sleep(2.5)

def search_github(username, password):
    opts = Options()
    #opts.add_argument('--headless')
    driver = webdriver.Chrome(options=opts)
    driver.get('https://github.com/search?l=KiCad+Schematic&q=EESchema+Schematic&type=Code')
    login(driver, username, password)

    page_batch_size = 10
    while True:
        for _ in range(page_batch_size):
            result_links = driver.find_elements_by_css_selector('.code-list-item .f4 a')
            for anchor in result_links:
                yield anchor.get_attribute('href')
            next_link = driver.find_element_by_css_selector('.next_page')
            has_next_page = next_link.tag_name == 'a'
            if has_next_page:
                next_url = next_link.get_attribute('href')
                driver.get(next_url)
            else:
                break
        print('----- taking a break for a bit... -----', file=sys.stderr)
        time.sleep(20)

    driver.quit()

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']
for file_url in search_github(username, password):
    print(file_url)
