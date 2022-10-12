import os,time,sys

from selenium import webdriver
from utils import prGreen,prRed,prYellow
from selenium.webdriver.common.keys import Keys

prYellow("ℹ️  This script will check if the bot can automatically log in Linkedin for you.")

def checkPython():
    try:
        if(sys.version):
            prGreen("✅ Python is succesfully installed!")
        else:
            prRed("❌ Python is not installed please install Python first: https://www.python.org/downloads/")
    except Exception as e:
        prRed(e)
def checkPip():
    try:
        import pip
        prGreen("✅ Pip is succesfully installed!")
    except ImportError:
        prRed("❌ Pip not present. Install pip: https://pip.pypa.io/en/stable/installation/")
def checkSelenium():
    try:
        import selenium
        prGreen("✅ Selenium is succesfully installed!")
    except ImportError:
        prRed("❌ Selenium not present. Install Selenium: https://pypi.org/project/selenium/")
def checkDotenv():
    try:
        import dotenv
        prGreen("✅ Dotenv is succesfully installed!")
    except ImportError:
        prRed("❌ Dotenv not present. Install Dotenv: https://pypi.org/project/python-dotenv/")


def checkSeleniumLinkedin():
    options = webdriver.FirefoxOptions()
    firefoxProfileRootDir = "/home/seluser/.mozilla/firefox/nrhpd5k5.linkbot"

    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument("-profile")
    options.add_argument(firefoxProfileRootDir)
    #options.headless = True

    browser = webdriver.Remote(
    command_executor='http://localhost:4000/wd/hub',
    options=options
    )

    try:
        browser.get('https://www.ongundemirag.com')
        if(browser.title.index("Ongun")>-1):
            prGreen("✅ Selenium and geckodriver is working succesfully!")
        else:
            prRed("❌ Please check if Selenium and geckodriver is installed")
    except Exception as e:
        prRed(e)

    try:
        browser.get('https://www.linkedin.com/feed/')
        time.sleep(3)
        if "Feed" in browser.title:
            prGreen('✅ Successfully you are logged in to Linkedin, you can now run main bot script!')
        else:
            prRed('❌ You are not automatically logged in, please set up your Firefox Account correctly.')         
            try:
                browser.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
                time.sleep(5)
                user_field = browser.find_element("id","username")
                pw_field = browser.find_element("id","password")
                login_button = browser.find_element("xpath",
                        '//*[@id="organic-div"]/form/div[3]/button')
                print(user_field, pw_field, login_button)
                # enter your linkedin username and  password below 
                username="linkedin@username.com"
                password="linkedin_password"
                user_field.send_keys(username)
                user_field.send_keys(Keys.TAB)
                time.sleep(2)
                pw_field.send_keys(password)
                time.sleep(2)
                login_button.click()
                time.sleep(3)
            except:
                raise Exception("Could not login!")   
                
    except Exception as e:
        prRed(e)
    finally:
        browser.quit()


checkPython()
checkPip()
checkSelenium()
checkDotenv()
checkSeleniumLinkedin()



print("Test Execution Successfully Completed!")