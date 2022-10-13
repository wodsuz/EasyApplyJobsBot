import time,os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

from ...LinkedinEasyApplyJobsBot.utils import printInfoMes,prYellow

class bot:
    def __init__(self):
        load_dotenv()
        self.driver = webdriver.Firefox(options=self.browser_options())

    def browser_options(self):
        options = Options()
        firefoxProfileRootDir = os.getenv('firefoxProfileRootDir')
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")

        options.add_argument("--disable-blink-features")
        #options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("-profile")
        options.add_argument(firefoxProfileRootDir)

        return options
    
    def mainBot(self):
        printInfoMes("AngelCo")


start = time.time()
bot().mainBot()
end = time.time()
prYellow("---Took: " + str(round((time.time() - start)/60)) + " minute(s).")
