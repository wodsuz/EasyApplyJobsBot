import constants

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


path = constants.firefoxAccountPath


options=Options()
options.set_preference('profile', path)
browser = webdriver.Firefox(options=options)
browser.get('https://www.ongundemirag.com')

print('Title: %s' % browser.title)

