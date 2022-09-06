import constants 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

print('This script will test if Selenium can automatically log in Linkedin for you.')

firefoxAccountPath = constants.firefoxAccountPath

options = Options()
options.add_argument("-profile")
options.add_argument(firefoxAccountPath)
browser = webdriver.Firefox(options=options)

try:
    browser.get('https://www.linkedin.com/feed/')
    if "Feed" in browser.title:
        print('✅ Successfully you are logged in, you can now run main bot script')
    else:
        print('❌ You are not automatically logged in, please set up your Firefox Account correctly.')
except Exception as e:
    print(e)
finally:
    browser.quit()


