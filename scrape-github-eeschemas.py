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

def search_github(username, password, page, end_page):
    opts = Options()
    opts.add_argument('--headless')
    driver = webdriver.Chrome(options=opts)
    driver.get(f'https://github.com/search?l=KiCad+Schematic&q=EESchema+Schematic&type=Code&p={page}')
    login(driver, username, password)

    for _ in range(page, end_page):
        links = driver.find_elements_by_css_selector('.code-list-item .f4 a')
        file_urls = [ link.get_attribute('href') for link in links ]
        for file_url in file_urls:
            yield file_url
        next_link = driver.find_element_by_css_selector('.next_page')
        has_next_page = next_link.tag_name == 'a'
        if has_next_page:
            next_url = next_link.get_attribute('href')
            driver.get(next_url)
        else:
            break
    driver.quit()

username = os.environ['GITHUB_USERNAME']
password = os.environ['GITHUB_PASSWORD']
start_page = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end_page = int(sys.argv[2]) if len(sys.argv) > 2 else start_page + 25
for file_url in search_github(username, password, start_page, end_page):
    print(file_url)
