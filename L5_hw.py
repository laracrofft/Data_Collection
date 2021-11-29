'''
Написать программу, которая собирает входящие письма из своего или тестового почтового ящика
и сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient

driver = webdriver.Chrome(executable_path=r'c:/Users/larch/chromedriver')

driver.get('https://mail.ru/')

elem = driver.find_element(By.XPATH, '//input[@name="login"]')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)

driver.implicitly_wait(1.5)

elem = driver.find_element(By.XPATH, '//input[@name="password"]')
elem.send_keys('NextPassword172#')
elem.send_keys(Keys.ENTER)

driver.implicitly_wait(10)

email_links = {}
new_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'js-letter-list-item')]")

for l in new_links:
        email_url = l.get_attribute('href')
        email_links[email_url] = l

# print(email_links)

client = MongoClient('localhost', 27017)
mongo_db = client['mailru']
inbox_letters = mongo_db.inbox_letters

for link in email_links:
    driver.get(link)
    letter_total = {}
    email_from = driver.find_element(By.XPATH, "//div[@class='letter__author']/span[@class='letter-contact']").text
    email_date = driver.find_element(By.XPATH, "//div[@class='letter__date']").text
    subject = driver.find_element(By.XPATH, "//h2[@class='thread__subject']").text
    letter = driver.find_element(By.XPATH, "//div[@class='letter__body']").text

    letter_total['from_'] = email_from
    letter_total['date'] = email_date
    letter_total['subject'] = subject
    letter_total['letter'] = letter

    inbox_letters.insert_one(letter_total)




