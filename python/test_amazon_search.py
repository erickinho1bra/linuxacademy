#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(executable_path='/Users/xelima/Documents/gitrepo/mybbprojects/files/chromedriver')
driver.implicitly_wait(5)

#driver.get('http://www.amazon.com/')
#
#search = driver.find_element(By.ID, 'twotabsearchtextbox')
#search.send_keys('tochi popcorn', Keys.ENTER)
#
#expected_text = '"tochi popcorn"'
#actual_text = driver.find_element(By.XPATH, "//span[@class='a-color-state a-text-bold']").text
#
#assert expected_text == actual_text, f'Error. Expected text:  {expected_text}, but actual text: {actual_text}'


driver.get('https://shop-staging.dccomics.com/')

#search = driver.find_element(By.XPATH, "//span[@class='a-color-state a-text-bold']")
#search.send_keys('tochi popcorn', Keys.ENTER)


#driver.quit()