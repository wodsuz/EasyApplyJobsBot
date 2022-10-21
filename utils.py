import math,constants,config
from typing import List
import time

from selenium.webdriver.firefox.options import Options

def browserOptions():
    options = Options()
    firefoxProfileRootDir = config.firefoxProfileRootDir
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-extensions")
    if(config.headless):
        options.add_argument("--headless")
    options.add_argument("--disable-blink-features")
    #options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("-profile")
    options.add_argument(firefoxProfileRootDir)

    return options

def prRed(prt):
    print(f"\033[91m{prt}\033[00m")

def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")

def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")

def getUrlDataFile():
    urlData = ""
    try:
        file = open('data/urlData.txt', 'r')
        urlData = file.readlines()
    except FileNotFoundError:
        text = "FileNotFound:urlData.txt file is not found. Please run ./jobPreferances/createUrl.py first and make sure you have urlData.txt in /data folder generated."
        prRed(text)
    return urlData

def jobsToPages(numOfJobs: str) -> int:
  number_of_pages = 1

  if (' ' in numOfJobs):
    spaceIndex = numOfJobs.index(' ')
    totalJobs = (numOfJobs[0:spaceIndex])
    totalJobs_int = int(totalJobs.replace(',', ''))
    number_of_pages = math.ceil(totalJobs_int/constants.jobsPerPage)
    if (number_of_pages > 40 ): number_of_pages = 40

  else:
      number_of_pages = int(numOfJobs)

  return number_of_pages

def urlToKeywords(url: str) -> List[str]:
    keyword = url[url.index("keywords=")+9:url.index("&location") ] 
    location = url[url.index("location=")+9:url.index("&f_E") ] 
    return [keyword,location]

def writeResults(text: str):
    timeStr = time.strftime("%Y%m%d")
    fileName = "Applied Jobs DATA - " +timeStr + ".txt"
    try:
        with open("data/" +fileName, encoding="utf-8" ) as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
                
        with open("data/" +fileName, 'w' ,encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )
            for line in lines: 
                f.write(line)
            f.write(text+ "\n")
            
    except:
        with open("data/" +fileName, 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " +timeStr+ "\n" )
            f.write("---- Job Title | Company | Location | Work Place | Posted Date | Applications | Result "   +"\n" )

            f.write(text+ "\n")

def printInfoMes(bot:str):
    prYellow("ℹ️ " +bot+ " is starting soon... ")

def donate(self):
    prYellow('If you like the project, please support me so that i can make more such projects, thanks!')
    try:
        self.driver.get('https://commerce.coinbase.com/checkout/923b8005-792f-4874-9a14-2992d0b30685')
    except Exception as e:
        prRed("Error in donate: " +str(e))