import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from dotenv import load_dotenv

print('This script will check if the bot can automatically log in Linkedin for you.')

load_dotenv()

options = Options()
firefoxProfilePath = os.getenv('firefoxProfilePath')

options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

# Disable webdriver flags or you will be easily detectable
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
# add profile 
options.add_argument("-profile")
options.add_argument(firefoxProfilePath)

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


