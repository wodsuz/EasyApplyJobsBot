import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from dotenv import load_dotenv

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
    browser.get('https://www.ongundemirag.com')
    if(browser.title.index("Ongun")>-1):
        print("✅ Selenium is working succesfully!")
    else:
        print("❌ Please check if Selenium is installed")
except Exception as e:
    print(e)
finally:
    browser.quit()

